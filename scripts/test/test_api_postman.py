#!/usr/bin/env python3
#
# GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
# Copyright (C) 2025 DTU-DZ2 Team
#
# Complete API Test Script - Tests ALL endpoints via API Gateway
#

"""
GreenEduMap API Test Script
Test ALL endpoints from ALL modules via API Gateway
Uses citizen1@gmail.com / password123 for authentication
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
        self.user_id = None
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0
        }
        self.failed_endpoints: List[Dict] = []
        self.tested_endpoints: List[Dict] = []
        
    def test_endpoint(self, name: str, method: str, endpoint: str, 
                     headers: Optional[Dict] = None, 
                     body: Optional[Dict] = None,
                     params: Optional[Dict] = None,
                     silent: bool = False,
                     require_auth: bool = True,
                     expected_fail: bool = False) -> bool:
        """Test a single endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            # Add auth header if token exists and required
            if headers is None:
                headers = {}
            if self.access_token and require_auth and "Authorization" not in headers:
                headers["Authorization"] = f"Bearer {self.access_token}"
            
            # Add content-type for POST/PUT/PATCH
            if method in ["POST", "PUT", "PATCH"] and body:
                headers["Content-Type"] = "application/json"
            
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
            
            # Record tested endpoint
            self.tested_endpoints.append({
                "name": name, "method": method, "endpoint": endpoint, 
                "status": response.status_code
            })
            
            # Check if successful (or expected fail)
            success = response.status_code < 400
            if expected_fail:
                success = response.status_code >= 400
                
            if success:
                self.test_results["passed"] += 1
                if not silent:
                    print(f"{Colors.GREEN}✓{Colors.ENDC} [{method}] {endpoint} - {response.status_code}")
                return True
            else:
                self.test_results["failed"] += 1
                error_detail = ""
                try:
                    error_data = response.json()
                    error_detail = error_data.get("detail", str(error_data))[:100]
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
                    print(f"{Colors.RED}✗{Colors.ENDC} [{method}] {endpoint} - {response.status_code}: {error_detail[:50]}")
                return False
                
        except Exception as e:
            self.test_results["failed"] += 1
            self.failed_endpoints.append({
                "name": name,
                "method": method,
                "endpoint": endpoint,
                "status": "ERROR",
                "error": str(e)[:100]
            })
            if not silent:
                print(f"{Colors.RED}✗{Colors.ENDC} [{method}] {endpoint} - Exception: {str(e)[:50]}")
            return False
    
    def login(self, email: str, password: str) -> bool:
        """Login and get access token"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/auth/login",
                json={"email": email, "password": password},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                self.refresh_token = data.get("refresh_token")
                
                # Get user ID
                me_response = requests.get(
                    f"{self.base_url}/api/v1/auth/me",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                    timeout=10
                )
                if me_response.status_code == 200:
                    self.user_id = me_response.json().get("id")
                return True
            return False
        except:
            return False
    
    def run_tests(self):
        """Run all API tests"""
        start_time = time.time()
        
        print(f"{Colors.BOLD}{Colors.BLUE}")
        print("╔════════════════════════════════════════════════════════════════════╗")
        print("║       GreenEduMap Complete API Test Suite                          ║")
        print("║       Testing ALL endpoints via API Gateway                        ║")
        print("╚════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        print(f"Base URL: {self.base_url}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # ================================
        # 1. Health Check & Root
        # ================================
        print(f"\n{Colors.CYAN}[1/12] Health & Root{Colors.ENDC}")
        self.test_endpoint("Root", "GET", "/", require_auth=False)
        self.test_endpoint("Health Check", "GET", "/health", require_auth=False)
        self.test_endpoint("Auth Health", "GET", "/api/v1/auth/health", require_auth=False)
        
        # ================================
        # 2. Authentication
        # ================================
        print(f"\n{Colors.CYAN}[2/12] Authentication (citizen1@gmail.com){Colors.ENDC}")
        if self.login("citizen1@gmail.com", "password123"):
            print(f"{Colors.GREEN}✓{Colors.ENDC} Login successful - User ID: {self.user_id[:8]}...")
            self.test_results["passed"] += 1
        else:
            print(f"{Colors.RED}✗{Colors.ENDC} Login failed")
            self.test_results["failed"] += 1
            self.failed_endpoints.append({
                "name": "Login", "method": "POST", 
                "endpoint": "/api/v1/auth/login", "status": "FAILED", "error": "Login failed"
            })
        
        self.test_endpoint("Get Current User", "GET", "/api/v1/auth/me")
        self.test_endpoint("Validate Token", "GET", "/api/v1/auth/validate-token")
        self.test_endpoint("Update Profile", "PATCH", "/api/v1/auth/profile", 
                          body={"full_name": "Test Citizen Updated"})
        
        # ================================
        # 3. FCM Tokens
        # ================================
        print(f"\n{Colors.CYAN}[3/12] FCM Token Management{Colors.ENDC}")
        self.test_endpoint("Register FCM Token", "POST", "/api/v1/auth/fcm-tokens",
                          body={"token": "test-fcm-token-123-android-device-2025", "device_type": "android"})
        self.test_endpoint("Update FCM Token (alias)", "POST", "/api/v1/auth/update-fcm-token",
                          body={"token": "test-fcm-token-456-ios-device-2025", "device_type": "ios"})
        self.test_endpoint("List FCM Tokens", "GET", "/api/v1/auth/fcm-tokens")
        
        # ================================
        # 4. User Data - Favorites
        # ================================
        print(f"\n{Colors.CYAN}[4/12] User Favorites{Colors.ENDC}")
        self.test_endpoint("List Favorites", "GET", "/api/v1/user-data/favorites")
        self.test_endpoint("List Favorites by Type", "GET", "/api/v1/user-data/favorites",
                          params={"target_type": "school"})
        
        # ================================
        # 5. User Data - Contributions
        # ================================
        print(f"\n{Colors.CYAN}[5/12] User Contributions{Colors.ENDC}")
        self.test_endpoint("List Contributions", "GET", "/api/v1/user-data/contributions")
        self.test_endpoint("List Public Contributions", "GET", "/api/v1/user-data/contributions/public",
                          require_auth=False)
        self.test_endpoint("Filter Contributions", "GET", "/api/v1/user-data/contributions",
                          params={"type": "feedback"})
        
        # ================================
        # 6. User Data - Activities & Settings
        # ================================
        print(f"\n{Colors.CYAN}[6/12] User Activities & Settings{Colors.ENDC}")
        self.test_endpoint("List Activities", "GET", "/api/v1/user-data/activities")
        self.test_endpoint("Get Settings", "GET", "/api/v1/user-data/settings")
        self.test_endpoint("Update Settings", "PUT", "/api/v1/user-data/settings",
                          body={"theme": "dark", "language": "vi"})
        
        # ================================
        # 7. Environment - Air Quality
        # ================================
        print(f"\n{Colors.CYAN}[7/12] Environment - Air Quality{Colors.ENDC}")
        self.test_endpoint("List Air Quality", "GET", "/api/v1/air-quality", params={"limit": 5})
        self.test_endpoint("Latest Air Quality", "GET", "/api/v1/air-quality/latest")
        
        # ================================
        # 8. Environment - Weather
        # ================================
        print(f"\n{Colors.CYAN}[8/12] Environment - Weather{Colors.ENDC}")
        self.test_endpoint("List Weather", "GET", "/api/v1/weather", params={"limit": 5})
        
        # ================================
        # 9. Education Service
        # ================================
        print(f"\n{Colors.CYAN}[9/12] Education Service{Colors.ENDC}")
        self.test_endpoint("List Schools", "GET", "/api/v1/schools", params={"limit": 5})
        self.test_endpoint("Nearby Schools", "GET", "/api/v1/schools/nearby", 
                          params={"latitude": 10.7769, "longitude": 106.7009, "radius_km": 10})
        self.test_endpoint("List Green Courses", "GET", "/api/v1/green-courses", params={"limit": 5})
        
        # ================================
        # 10. Resource Service  
        # ================================
        print(f"\n{Colors.CYAN}[10/12] Resource Service{Colors.ENDC}")
        self.test_endpoint("List Green Zones", "GET", "/api/v1/green-zones", params={"limit": 5})
        self.test_endpoint("Nearby Green Zones", "GET", "/api/v1/green-zones/nearby",
                          params={"latitude": 10.7769, "longitude": 106.7009, "radius_km": 10})
        self.test_endpoint("List Green Resources", "GET", "/api/v1/green-resources", params={"limit": 5})
        self.test_endpoint("List Centers", "GET", "/api/v1/centers", params={"limit": 5})
        
        # ================================
        # 11. Public Open Data (No Auth Required)
        # ================================
        print(f"\n{Colors.CYAN}[11/12] Public Open Data (No Auth){Colors.ENDC}")
        self.test_endpoint("Public Air Quality", "GET", "/api/open-data/air-quality", 
                          params={"limit": 5}, require_auth=False)
        self.test_endpoint("Public AQI by Location", "GET", "/api/open-data/air-quality/location",
                          params={"lat": 10.7769, "lon": 106.7009, "radius": 50}, require_auth=False)
        self.test_endpoint("Public Weather", "GET", "/api/open-data/weather/current",
                          params={"city": "TP. Hồ Chí Minh"}, require_auth=False)
        self.test_endpoint("Weather Forecast", "GET", "/api/open-data/weather/forecast",
                          params={"city": "Đà Nẵng"}, require_auth=False)
        self.test_endpoint("Public Green Zones", "GET", "/api/open-data/green-zones", 
                          params={"limit": 5}, require_auth=False)
        self.test_endpoint("Public Green Resources", "GET", "/api/open-data/green-resources", 
                          params={"limit": 5}, require_auth=False)
        self.test_endpoint("Public Centers", "GET", "/api/open-data/centers", 
                          params={"limit": 5}, require_auth=False)
        self.test_endpoint("Centers Nearby", "GET", "/api/open-data/centers/nearby",
                          params={"latitude": 10.7769, "longitude": 106.7009}, require_auth=False)
        self.test_endpoint("Data Catalog", "GET", "/api/open-data/catalog", require_auth=False)
        self.test_endpoint("Export Air Quality", "GET", "/api/open-data/export/air-quality",
                          params={"format": "json"}, require_auth=False)
        
        # ================================
        # 12. Education Open Data
        # ================================
        print(f"\n{Colors.CYAN}[12/12] Education Open Data{Colors.ENDC}")
        self.test_endpoint("Public Schools", "GET", "/api/open-data/schools", 
                          params={"limit": 5}, require_auth=False)
        self.test_endpoint("Public Green Courses", "GET", "/api/open-data/green-courses",
                          params={"limit": 5}, require_auth=False)
        
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
                print(f"{i}. {Colors.BOLD}[{failed['method']}]{Colors.ENDC} {failed['endpoint']}")
                print(f"   Name: {failed['name']}")
                print(f"   Status: {Colors.RED}{failed['status']}{Colors.ENDC}")
                print(f"   Error: {failed['error'][:80]}")
                print()
        
        # Print endpoint summary table
        print(f"\n{Colors.BOLD}Tested Endpoints by Category:{Colors.ENDC}")
        categories = {
            "Health": [e for e in self.tested_endpoints if "/health" in e["endpoint"] or e["endpoint"] == "/"],
            "Auth Core": [e for e in self.tested_endpoints if "/auth/" in e["endpoint"] and "fcm" not in e["endpoint"] and "user" not in e["endpoint"]],
            "FCM Tokens": [e for e in self.tested_endpoints if "fcm" in e["endpoint"]],
            "User Data": [e for e in self.tested_endpoints if "/user-data/" in e["endpoint"]],
            "Air Quality": [e for e in self.tested_endpoints if "/air-quality" in e["endpoint"]],
            "Weather": [e for e in self.tested_endpoints if "/weather" in e["endpoint"]],
            "Education": [e for e in self.tested_endpoints if "/schools" in e["endpoint"] or "/green-courses" in e["endpoint"]],
            "Resources": [e for e in self.tested_endpoints if "/green-zones" in e["endpoint"] or "/green-resources" in e["endpoint"] or "/centers" in e["endpoint"]],
            "Open Data": [e for e in self.tested_endpoints if "/open-data/" in e["endpoint"]],
        }
        
        for category, endpoints in categories.items():
            if endpoints:
                passed = sum(1 for e in endpoints if e["status"] < 400)
                status_icon = "✅" if passed == len(endpoints) else "⚠️"
                print(f"  {status_icon} {category}: {passed}/{len(endpoints)}")

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
