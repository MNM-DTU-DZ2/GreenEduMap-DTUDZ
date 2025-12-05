"""
GreenEduMap API Full Test Suite
Tests all API endpoints with comprehensive coverage
"""

import requests
import json
import time
from typing import Dict, Optional
from datetime import datetime

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'skipped': 0
        }
        
    def print_header(self, text: str):
        """Print section header"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")
        
    def print_test(self, name: str, status: str, details: str = ""):
        """Print test result"""
        if status == "PASS":
            icon = "✓"
            color = Colors.GREEN
            self.test_results['passed'] += 1
        elif status == "FAIL":
            icon = "✗"
            color = Colors.RED
            self.test_results['failed'] += 1
        else:
            icon = "○"
            color = Colors.YELLOW
            self.test_results['skipped'] += 1
            
        print(f"{color}{icon} {name}{Colors.RESET}")
        if details:
            print(f"  {Colors.YELLOW}└─ {details}{Colors.RESET}")
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with optional authentication"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        
        if self.access_token and 'Authorization' not in headers:
            headers['Authorization'] = f"Bearer {self.access_token}"
            
        kwargs['headers'] = headers
        
        try:
            response = requests.request(method, url, **kwargs)
            return response
        except Exception as e:
            print(f"{Colors.RED}Request failed: {str(e)}{Colors.RESET}")
            raise
    
    def test_endpoint(self, name: str, method: str, endpoint: str, 
                     expected_status: int = 200, **kwargs) -> bool:
        """Test a single endpoint"""
        try:
            response = self.make_request(method, endpoint, **kwargs)
            
            if response.status_code == expected_status:
                self.print_test(name, "PASS", f"Status: {response.status_code}")
                return True
            else:
                self.print_test(name, "FAIL", 
                              f"Expected {expected_status}, got {response.status_code}")
                return False
        except Exception as e:
            self.print_test(name, "FAIL", f"Error: {str(e)}")
            return False
    
    # ========================================
    # Authentication Tests
    # ========================================
    
    def test_authentication(self):
        """Test all authentication endpoints"""
        self.print_header("1. AUTHENTICATION TESTS")
        
        # Test Register
        register_data = {
            "email": f"test_{int(time.time())}@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User",
            "phone": "+84901234567"
        }
        
        response = self.make_request(
            "POST", 
            "/api/v1/auth/register",
            json=register_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            data = response.json()
            if 'access_token' in data:
                self.access_token = data['access_token']
                self.refresh_token = data.get('refresh_token')
                self.print_test("Register", "PASS", "User created and tokens saved")
            else:
                self.print_test("Register", "FAIL", "No token in response")
        else:
            self.print_test("Register", "FAIL", f"Status: {response.status_code}")
        
        # Test Login
        login_data = {
            "email": register_data['email'],
            "password": register_data['password']
        }
        
        response = self.make_request(
            "POST",
            "/api/v1/auth/login",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access_token', self.access_token)
            self.print_test("Login", "PASS", "Logged in successfully")
        else:
            self.print_test("Login", "FAIL", f"Status: {response.status_code}")
        
        # Test Get Current User
        self.test_endpoint("Get Current User", "GET", "/api/v1/auth/me")
        
        # Test Update Profile
        update_data = {
            "full_name": "Updated Test User",
            "phone": "+84909999999"
        }
        self.test_endpoint(
            "Update Profile", 
            "PUT", 
            "/api/v1/auth/profile",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Test Refresh Token
        if self.refresh_token:
            self.test_endpoint(
                "Refresh Token",
                "POST",
                "/api/v1/auth/refresh",
                json={"refresh_token": self.refresh_token},
                headers={'Content-Type': 'application/json'}
            )
    
    # ========================================
    # Environment Data Tests
    # ========================================
    
    def test_environment_data(self):
        """Test environment data endpoints"""
        self.print_header("2. ENVIRONMENT DATA TESTS")
        
        # Air Quality
        self.test_endpoint("Get Air Quality Data", "GET", "/api/v1/air-quality?skip=0&limit=10")
        self.test_endpoint("Get Latest Air Quality", "GET", "/api/v1/air-quality/latest?limit=10")
        self.test_endpoint("Get Air Quality by ID", "GET", "/api/v1/air-quality/1", expected_status=200)
        
        # Weather
        self.test_endpoint("Get Weather Data", "GET", "/api/v1/weather?skip=0&limit=10")
        self.test_endpoint("Get Current Weather", "GET", "/api/v1/weather/current?city=Ho Chi Minh City")
    
    # ========================================
    # Education Data Tests
    # ========================================
    
    def test_education_data(self):
        """Test education data endpoints"""
        self.print_header("3. EDUCATION DATA TESTS")
        
        # Schools
        self.test_endpoint("Get Schools", "GET", "/api/v1/schools?skip=0&limit=10")
        self.test_endpoint(
            "Get Nearby Schools", 
            "GET", 
            "/api/v1/schools/nearby?latitude=10.7769&longitude=106.7009&radius=5&limit=10"
        )
        self.test_endpoint("Get School by ID", "GET", "/api/v1/schools/1", expected_status=200)
        
        # Green Courses
        self.test_endpoint("Get Green Courses", "GET", "/api/v1/green-courses?skip=0&limit=10")
    
    # ========================================
    # Green Resources Tests
    # ========================================
    
    def test_green_resources(self):
        """Test green resources endpoints"""
        self.print_header("4. GREEN RESOURCES TESTS")
        
        # Temporarily remove auth for public endpoints
        temp_token = self.access_token
        self.access_token = None
        
        self.test_endpoint("Get Green Zones", "GET", "/api/open-data/green-zones?skip=0&limit=10")
        self.test_endpoint(
            "Get Nearby Green Zones",
            "GET",
            "/api/open-data/green-zones/nearby?latitude=10.7769&longitude=106.7009&radius=5"
        )
        self.test_endpoint("Get Green Resources", "GET", "/api/open-data/green-resources?skip=0&limit=10")
        
        # Restore auth token
        self.access_token = temp_token
    
    # ========================================
    # Public Endpoints Tests
    # ========================================
    
    def test_public_endpoints(self):
        """Test public endpoints (no authentication)"""
        self.print_header("5. PUBLIC ENDPOINTS TESTS")
        
        # Temporarily remove auth
        temp_token = self.access_token
        self.access_token = None
        
        self.test_endpoint("Public Air Quality", "GET", "/api/open-data/air-quality?limit=10")
        self.test_endpoint("Public Current Weather", "GET", "/api/open-data/weather/current?city=Ho Chi Minh City")
        self.test_endpoint("Public Weather Forecast", "GET", "/api/open-data/weather/forecast?city=Ho Chi Minh City")
        self.test_endpoint("Get Catalog", "GET", "/api/open-data/catalog")
        
        # Restore auth token
        self.access_token = temp_token
    
    # ========================================
    # AI Tasks Tests
    # ========================================
    
    def test_ai_tasks(self):
        """Test AI task endpoints"""
        self.print_header("6. AI TASKS TESTS")
        
        # Clustering Task
        clustering_data = {
            "data_type": "environment",
            "n_clusters": 3,
            "method": "kmeans"
        }
        self.test_endpoint(
            "Queue Clustering Task",
            "POST",
            "/api/v1/tasks/ai/clustering",
            json=clustering_data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Prediction Task
        prediction_data = {
            "prediction_type": "air_quality",
            "location_id": "test_location"
        }
        self.test_endpoint(
            "Queue Prediction Task",
            "POST",
            "/api/v1/tasks/ai/prediction",
            json=prediction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Correlation Task
        correlation_data = {
            "analysis_type": "pearson"
        }
        self.test_endpoint(
            "Queue Correlation Task",
            "POST",
            "/api/v1/tasks/ai/correlation",
            json=correlation_data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Export Task
        export_data = {
            "data_type": "schools",
            "format": "csv"
        }
        self.test_endpoint(
            "Queue Export Task",
            "POST",
            "/api/v1/tasks/export",
            json=export_data,
            headers={'Content-Type': 'application/json'}
        )
    
    # ========================================
    # Health Check Tests
    # ========================================
    
    def test_health_check(self):
        """Test health check endpoint"""
        self.print_header("7. HEALTH CHECK TESTS")
        
        # Temporarily remove auth
        temp_token = self.access_token
        self.access_token = None
        
        response = self.make_request("GET", "/health")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'unknown')
            
            if status == 'healthy':
                self.print_test("Health Check", "PASS", f"Status: {status}")
            else:
                self.print_test("Health Check", "PASS", f"Status: {status} (degraded)")
                
            # Print service statuses
            services = data.get('services', {})
            for service, service_status in services.items():
                color = Colors.GREEN if service_status == 'healthy' else Colors.YELLOW
                print(f"  {color}├─ {service}: {service_status}{Colors.RESET}")
        else:
            self.print_test("Health Check", "FAIL", f"Status: {response.status_code}")
        
        # Restore auth token
        self.access_token = temp_token
    
    # ========================================
    # Run All Tests
    # ========================================
    
    def run_all_tests(self):
        """Run all test suites"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}GreenEduMap API Full Test Suite{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}Base URL: {self.base_url}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
        
        start_time = time.time()
        
        try:
            self.test_authentication()
            self.test_environment_data()
            self.test_education_data()
            self.test_green_resources()
            self.test_public_endpoints()
            self.test_ai_tasks()
            self.test_health_check()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
        except Exception as e:
            print(f"\n{Colors.RED}Test suite failed: {str(e)}{Colors.RESET}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        self.print_summary(duration)
    
    def print_summary(self, duration: float):
        """Print test summary"""
        total = sum(self.test_results.values())
        passed = self.test_results['passed']
        failed = self.test_results['failed']
        skipped = self.test_results['skipped']
        
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}TEST SUMMARY{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Passed:  {passed}{Colors.RESET}")
        print(f"{Colors.RED}✗ Failed:  {failed}{Colors.RESET}")
        print(f"{Colors.YELLOW}○ Skipped: {skipped}{Colors.RESET}")
        print(f"{Colors.BOLD}Total:     {total}{Colors.RESET}")
        print(f"{Colors.BOLD}Pass Rate: {pass_rate:.1f}%{Colors.RESET}")
        print(f"{Colors.BOLD}Duration:  {duration:.2f}s{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")
        
        if failed == 0:
            print(f"{Colors.BOLD}{Colors.GREEN}🎉 ALL TESTS PASSED!{Colors.RESET}\n")
        else:
            print(f"{Colors.BOLD}{Colors.RED}⚠️  SOME TESTS FAILED{Colors.RESET}\n")


def main():
    """Main entry point"""
    import sys
    
    # Default to production URL
    base_url = "https://api.greenedumap.io.vn"
    
    # Allow override via command line
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"\n{Colors.BOLD}Testing API at: {base_url}{Colors.RESET}\n")
    
    tester = APITester(base_url)
    tester.run_all_tests()


if __name__ == "__main__":
    main()
