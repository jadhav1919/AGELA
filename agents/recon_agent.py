import requests
import urllib3
from bs4 import BeautifulSoup
from core.base_agent import BaseAgent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ReconAgent(BaseAgent):
    """
    Recon Agent — fingerprints the target web application.
    Discovers: tech stack, forms, endpoints, headers, links.
    Auto-logs into DVWA for authenticated scanning.
    """

    def __init__(self, model: str = "mistral"):
        super().__init__(name="ReconAgent", model=model)

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "AGELA-Security-Scanner/1.0 (Authorized Testing)"
        })

        self._dvwa_login()

    def _dvwa_login(self):
        """Auto-login to DVWA and set security to low"""

        try:
            # Get login page and extract CSRF token
            login_page = self.session.get(
                "http://localhost/login.php",
                verify=False,
                timeout=10
            )

            soup = BeautifulSoup(login_page.text, "html.parser")

            token = soup.find(
                "input",
                {"name": "user_token"}
            )

            user_token = token["value"] if token else ""

            # Submit login form
            self.session.post(
                "http://localhost/login.php",
                data={
                    "username": "admin",
                    "password": "password",
                    "Login": "Login",
                    "user_token": user_token
                },
                verify=False,
                timeout=10
            )

            # Set security level to low
            self.session.cookies.update({
                "security": "low"
            })

            self.log("✓ DVWA auto-login successful")

        except Exception as e:
            self.log(f"DVWA login failed: {str(e)}")

    def fetch_page(self, url: str) -> tuple:
        """Fetch a page and return (response, soup)"""

        try:
            response = self.session.get(
                url,
                timeout=10,
                verify=False
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            return response, soup

        except Exception as e:
            self.log(
                f"Failed to fetch {url}: {str(e)}"
            )

            return None, None

    def extract_headers(self, response) -> dict:
        """Extract and analyze HTTP response headers"""

        if not response:
            return {}

        headers = dict(response.headers)
        tech_indicators = {}

        if "X-Powered-By" in headers:
            tech_indicators["powered_by"] = headers["X-Powered-By"]

        if "Server" in headers:
            tech_indicators["server"] = headers["Server"]

        if "X-Generator" in headers:
            tech_indicators["generator"] = headers["X-Generator"]

        if "Set-Cookie" in headers:
            tech_indicators["cookies"] = headers["Set-Cookie"]

        return {
            "all_headers": headers,
            "tech_indicators": tech_indicators
        }

    def extract_forms(self, soup) -> list:
        """Find all forms and their input fields"""

        if not soup:
            return []

        forms = []

        for form in soup.find_all("form"):

            form_data = {
                "action": form.get("action", ""),
                "method": form.get("method", "GET").upper(),
                "inputs": []
            }

            for inp in form.find_all(
                ["input", "textarea", "select"]
            ):

                form_data["inputs"].append({
                    "name": inp.get("name", ""),
                    "type": inp.get("type", "text"),
                    "value": inp.get("value", "")
                })

            forms.append(form_data)

        return forms

    def extract_links(self, soup, base_url: str) -> list:
        """Extract all internal links"""

        if not soup:
            return []

        links = []

        for a in soup.find_all(
            "a",
            href=True
        ):

            href = a["href"]

            if href.startswith("http"):

                if base_url in href:
                    links.append(href)

            elif href.startswith("/"):

                links.append(
                    base_url.rstrip("/") + href
                )

        return list(set(links))[:20]

    def detect_tech_stack(self, response, soup) -> dict:
        """Detect CMS, framework and language from page content"""

        tech = {
            "cms": "unknown",
            "language": "unknown",
            "framework": "unknown",
            "database": "unknown"
        }

        if not response or not soup:
            return tech

        page_text = response.text.lower()

        # CMS detection
        if (
            "wp-content" in page_text
            or "wordpress" in page_text
        ):
            tech["cms"] = "WordPress"

        elif "joomla" in page_text:
            tech["cms"] = "Joomla"

        elif "drupal" in page_text:
            tech["cms"] = "Drupal"

        elif "dvwa" in page_text:
            tech["cms"] = "DVWA"

        # Language detection
        powered_by = response.headers.get(
            "X-Powered-By",
            ""
        ).lower()

        if "php" in powered_by:
            tech["language"] = "PHP"

        elif "asp" in powered_by:
            tech["language"] = "ASP.NET"

        # Framework detection
        server = response.headers.get(
            "Server",
            ""
        ).lower()

        if "apache" in server:
            tech["framework"] = "Apache"

        elif "nginx" in server:
            tech["framework"] = "Nginx"

        elif "iis" in server:
            tech["framework"] = "IIS"

        # Database hints
        if "mysql" in page_text:
            tech["database"] = "MySQL"

        elif "postgresql" in page_text:
            tech["database"] = "PostgreSQL"

        return tech

    def run(self, context: dict) -> dict:

        target_url = context["target_url"]

        self.log(
            f"Starting reconnaissance on: {target_url}"
        )

        response, soup = self.fetch_page(
            target_url
        )

        if not response:

            self.log(
                "Failed to reach target — "
                "check if DVWA is running"
            )

            context["recon"] = {
                "error": "Target unreachable"
            }

            return context

        self.log(
            f"Target responded with HTTP "
            f"{response.status_code}"
        )

        headers = self.extract_headers(
            response
        )

        forms = self.extract_forms(
            soup
        )

        links = self.extract_links(
            soup,
            target_url
        )

        tech = self.detect_tech_stack(
            response,
            soup
        )

        recon_data = {
            "url": target_url,
            "status_code": response.status_code,
            "headers": headers,
            "forms": forms,
            "links": links,
            "tech_stack": tech,
            "page_title": (
                soup.title.string
                if soup.title
                else "unknown"
            ),
            "forms_count": len(forms),
            "links_count": len(links)
        }

        self.log(
            f"Found {len(forms)} forms "
            f"and {len(links)} links"
        )

        self.log(
            f"Detected tech: {tech}"
        )

        # Diagnostic: show discovered form inputs
        for index, form in enumerate(forms, start=1):

            input_names = [
                inp.get("name", "")
                for inp in form.get("inputs", [])
                if inp.get("name", "")
            ]

            self.log(
                f"Form {index} inputs: "
                f"{input_names}"
            )

        system_prompt = """You are a security reconnaissance expert.
Analyze web application fingerprint data and identify potential
attack vectors. Be specific and technical."""

        prompt = f"""
Based on this reconnaissance data, identify the most promising attack vectors:

Tech Stack: {tech}
Forms found: {len(forms)}
Form details: {forms[:3]}
HTTP Headers: {headers.get('tech_indicators', {})}
Page title: {recon_data['page_title']}

List the top attack vectors in order of likelihood:
"""

        llm_analysis = self.think(
            prompt,
            system_prompt
        )

        recon_data["llm_analysis"] = llm_analysis

        context["recon"] = recon_data

        self.log(
            "Reconnaissance complete"
        )

        return context