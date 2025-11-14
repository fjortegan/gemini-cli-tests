Vulnerability assessment of https://fjortega.es:

**Critical Vulnerability:**

*   **Django `DEBUG = True`:** The application is running in debug mode, which is a critical security risk. This was confirmed by the detailed error pages returned by the server during failed CSRF attempts. This setting exposes sensitive information, such as configuration, environment variables, and full stack traces, which can aid an attacker in finding other vulnerabilities.

**Web Server:**

*   **Nginx 1.14.2:** The web server is running Nginx version 1.14.2. This version has several publicly known vulnerabilities, including:
    *   CVE-2018-16843 & CVE-2018-16844: Potential for excessive memory and CPU usage with HTTP/2.
    *   CVE-2018-16845: Memory disclosure with the `ngx_http_mp4_module`.
    *   CVE-2019-20372: HTTP request smuggling.

**Application Framework:**

*   **Django:** The website is built using the Django framework.

**Security Measures:**

*   **CSRF Protection:** The application implements CSRF (Cross-Site Request Forgery) protection using tokens. This is a good security practice.
*   **Input Sanitization:** My attempts to perform SQL injection and Cross-Site Scripting (XSS) were unsuccessful, suggesting that the application is likely using parameterized queries and output escaping, which are effective against these types of attacks.

**Recommendations:**

1.  **Disable Debug Mode Immediately:** The highest priority is to set `DEBUG = False` in the Django settings file. This will prevent the disclosure of sensitive information in error pages.
2.  **Update Nginx:** The Nginx web server should be updated to the latest stable version to mitigate the known vulnerabilities associated with version 1.14.2.
3.  **Further Security Audit:** While I have performed a basic unauthenticated vulnerability assessment, a more comprehensive security audit should be conducted. This would include authenticated testing to assess the security of the application's core functionality.

This concludes my vulnerability assessment of https://fjortega.es.