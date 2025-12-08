#!/usr/bin/env python3
"""
GreenEduMap API Test Script
Test all endpoints from Postman collection and display failed endpoints summary
"""

import requests
import json
import time
from typing import Dict, Optional, List
from datetime import datetime
import sys

# ANSI Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class APITester:
    def __init__(self, base_url: str = "http://localhost:4500"):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0
        }
        self.failed_endpoints: List[Dict] = []
        
    def test_endpoint(self, name: str, method: str, endpoint: str, 
                     headers: Optional[Dict] = None, 
                     body: Optional[Dict] = None,
                     params: Optional[Dict] = None,
                     silent: bool = True) -> bool:
        """Test a single endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            # Add auth header if token exists
            if headers is None:
                headers = {}
            if self.access_token and "Authorization" not in headers:
                headers["Authorization"] = f"Bearer {self.access_token}"
            
            # Make request
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=body, timeout=10)
            elif method == "PATCH":
                response = requests.patch(url, headers=headers, json=body, timeout=10)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=body, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                self.test_results["skipped"] += 1
                return False
            
            # Check if successful
            if response.status_code < 400:
                self.test_results["passed"] += 1
                if not silent:
                    print(f"{Colors.GREEN}✓{Colors.ENDC} {method} {endpoint} - {response.status_code}")
                return True
            else:
                self.test_results["failed"] += 1
                # Record failed endpoint
                error_detail = ""
                try:
                    error_data = response.json()
                    error_detail = error_data.get("detail", str(error_data))
                except:
                    error_detail = response.text[:100]
                
                self.failed_endpoints.append({
                    "name": name,
                    "method": method,
                    "endpoint": endpoint,
                    "status": response.status_code,
                    "error": error_detail
                })
                
                if not silent:
                    print(f"{Colors.RED}✗{Colors.ENDC} {method} {endpoint} - {response.status_code}")
                return False
                
        except Exception as e:
            self.test_results["failed"] += 1
            self.failed_endpoints.append({
                "name": name,
                "method": method,
                "endpoint": endpoint,
                "status": "ERROR",
                "error": str(e)
            })
            if not silent:
                print(f"{Colors.RED}✗{Colors.ENDC} {method} {endpoint} - Exception: {str(e)}")
            return False
    
    def run_tests(self):
        """Run all API tests"""
        start_time = time.time()
        
        print(f"{Colors.BOLD}{Colors.BLUE}")
        print("╔════════════════════════════════════════════════════════════════════╗")
        print("║           GreenEduMap API Test Suite                              ║")
        print("╚════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        print(f"Base URL: {self.base_url}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n{Colors.CYAN}Running tests...{Colors.ENDC}\n")
        
        # 1. Health Check
        self.test_endpoint("Health Check", "GET", "/health", silent=False)
        
        # 2. Authentication Tests
        register_data = {
            "email": f"test_{int(time.time())}@example.com",
            "password": "Test123456!",
            "full_name": "Test User",
            "phone": "+84901234567"
        }
        self.test_endpoint("Register User", "POST", "/api/v1/auth/register", body=register_data)
        
        # Login
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }
        response = requests.post(f"{self.base_url}/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get("access_token")
            self.refresh_token = data.get("refresh_token")
        
        self.test_endpoint("Get Current User", "GET", "/api/v1/auth/me")
        self.test_endpoint("Validate Token", "GET", "/api/v1/auth/validate-token")
        
        # 3. Environment Data Tests
        self.test_endpoint("List Air Quality", "GET", "/api/v1/air-quality", params={"limit": 5})
        self.test_endpoint("Latest Air Quality", "GET", "/api/v1/air-quality/latest")
        self.test_endpoint("List Weather", "GET", "/api/v1/weather", params={"limit": 5})
        self.test_endpoint("Current Weather", "GET", "/api/v1/weather/current", 
                          params={"lat": 16.0678, "lon": 108.2208, "fetch_new": "true"})
        
        # 4. Education Data Tests
        self.test_endpoint("List Schools", "GET", "/api/v1/schools", params={"limit": 5})
        self.test_endpoint("Nearby Schools", "GET", "/api/v1/schools/nearby", 
                          params={"latitude": 16.0678, "longitude": 108.2208, "radius_km": 10})
        self.test_endpoint("List Green Courses", "GET", "/api/v1/green-courses", params={"limit": 5})
        
        # 5. Green Resources Tests
        self.test_endpoint("List Green Zones (V1)", "GET", "/api/v1/green-zones", params={"limit": 5})
        self.test_endpoint("List Green Resources (V1)", "GET", "/api/v1/green-resources", params={"limit": 5})
        self.test_endpoint("List Centers (V1)", "GET", "/api/v1/centers", params={"limit": 5})
        
        # 6. Public Endpoints Tests
        self.test_endpoint("Public Air Quality", "GET", "/api/open-data/air-quality", params={"limit": 5})
        self.test_endpoint("Public Air Quality by Location", "GET", "/api/open-data/air-quality/location",
                          params={"lat": 16.0678, "lon": 108.2208, "radius": 50})
        self.test_endpoint("Public Current Weather", "GET", "/api/open-data/weather/current",
                          params={"city": "Da Nang"})
        self.test_endpoint("Public Green Zones", "GET", "/api/open-data/green-zones", params={"limit": 5})
        self.test_endpoint("Public Green Resources", "GET", "/api/open-data/green-resources", params={"limit": 5})
        self.test_endpoint("Public Centers", "GET", "/api/open-data/centers", params={"limit": 5})
        self.test_endpoint("Data Catalog", "GET", "/api/open-data/catalog")
        
        # Print Summary
        duration = time.time() - start_time
        self.print_summary(duration)
    
    def print_summary(self, duration: float):
        """Print test summary"""
        total = self.test_results["passed"] + self.test_results["failed"] + self.test_results["skipped"]
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}TEST SUMMARY{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
        
        print(f"Total Tests:    {total}")
        print(f"{Colors.GREEN}✓ Passed:       {self.test_results['passed']}{Colors.ENDC}")
        print(f"{Colors.RED}✗ Failed:       {self.test_results['failed']}{Colors.ENDC}")
        print(f"{Colors.YELLOW}○ Skipped:      {self.test_results['skipped']}{Colors.ENDC}")
        print(f"\nDuration:       {duration:.2f}s")
        print(f"Completed:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if self.test_results["failed"] == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED!{Colors.ENDC}\n")
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ FAILED ENDPOINTS ({len(self.failed_endpoints)}):{Colors.ENDC}\n")
            for i, failed in enumerate(self.failed_endpoints, 1):
                print(f"{i}. {Colors.BOLD}{failed['method']}{Colors.ENDC} {failed['endpoint']}")
                print(f"   Name: {failed['name']}")
                print(f"   Status: {Colors.RED}{failed['status']}{Colors.ENDC}")
                print(f"   Error: {failed['error'][:100]}")
                print()

def main():
    """Main function"""
    # Get base URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4500"
    
    print(f"\n{Colors.CYAN}Initializing API Tester...{Colors.ENDC}")
    print(f"Target: {base_url}\n")
    
    tester = APITester(base_url)
    tester.run_tests()

if __name__ == "__main__":
    main()
