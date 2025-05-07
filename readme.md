# The User Management System Final Project:

# My Experience with the course and project:
Enrolling in this course has been an incredibly rewarding and eye-opening journey for me as a budding software engineer. Kicking off with the Advanced Python Calculator App, I developed a solid grasp of writing clean, maintainable Python code while immersing myself in key software engineering principles. Working on this project exposed me to practical uses of design patterns like Facade and Command, maintaining calculation history with Pandas, creating a modular plugin system for future scalability, and configuring robust logging mechanisms using environment variables. Setting up GitHub Actions for continuous testing and ensuring adherence to PEP8 standards allowed me to experience industry-grade development practices firsthand.
Progressing to the User Management System was a major step up in complexity and scope. This ambitious project challenged me to design and build RESTful APIs using FastAPI, structure data with SQLAlchemy and PostgreSQL, and tackle real-world backend problems like secure authentication, role-based access control, and dynamic search with pagination. Successfully deploying the application using Docker and DockerHub marked a proud milestone, giving me hands-on experience with containerization and modern deployment workflows. The iterative process of debugging, addressing QA feedback, and writing comprehensive tests with Pytest further strengthened my understanding of automated testing and clean version control.
Both projects provided immersive, practical exposure to backend development, database modeling, testing, and deployment. Beyond technical skills, this course helped me cultivate a logical, solution-driven approach to problem-solving and the confidence to take on intricate, real-world challenges. I now feel well-prepared—and genuinely excited—to apply these capabilities in future roles within software development and data engineering.

# Closed GitHub Issues (QA Improvements):

Issue 1:
Title: generating-nickname
Issue Link: Link
Commit Link: Link

Issue 2:
Title: strengthening-security
Issue Link: Link
Commit Link: Link

Issue 3:
Title: fix-dockerfile-allow-build
Issue Link: Link
Commit Link: Link
Issue 4:
Title: profile-picture-url-validation
Issue Link: Link
Commit Link: Link

Issue 5:
Title: validating-password
Issue Link: Link
Commit Link: Link

# 10 New Tests Created and Merged:

A Deep Dive into the Profile Picture Upload Feature
Contributing to this feature was a deeply satisfying and technically enriching experience. I meticulously designed and executed a comprehensive suite of 10+ test cases to thoroughly validate every critical aspect of the profile picture upload functionality. This testing phase not only ensured high reliability and usability but also reinforced seamless integration with the MinIO backend for secure, performant file handling.

Testing Strategy
Thorough Coverage: From standard operations to edge cases, all scenarios—such as valid uploads, improper file formats, and backend failures—were scrutinized through carefully constructed test cases.
Robust Validation: Focused on key factors like file type enforcement, size limits, naming conventions, and API consistency.
Resilient Backend Handling: Tested the MinIO integration with both positive and failure-mode simulations to ensure fault tolerance and graceful degradation.


Detailed Test Case Descriptions
1. Unsupported File Type Upload
Name: test_upload_profile_picture_invalid_file_type
Goal: Prevent non-image files from being accepted (e.g., .txt files).
Expected Result: Raises ValueError stating "Unsupported file type".
Link Here


2. Successful File Upload
Name: test_upload_profile_picture_success
Goal: Upload a valid .jpg file and verify correct MinIO interaction.
Expected Result: File uploads successfully; returns valid public URL.
Link Here

3. Generate URL for Existing File
Name: test_get_profile_picture_url_success
Goal: Retrieve a presigned URL for an existing file.
Expected Result: Correct URL is returned using MinIO's signing method.
Link Here

4. Handle Missing File Retrieval
Name: test_get_profile_picture_url_non_existent_file
Goal: Confirm proper error handling when a file is not found.
Expected Result: Raises "File not found" exception.
Link Here

5. Upload of Large Files
Name: test_upload_profile_picture_large_file
Goal: Test upload robustness for a ~20MB file.
Expected Result: Upload completes without error, with valid URL.
Link Here

6. Invalid Bucket Scenario
Name: test_get_profile_picture_url_invalid_bucket
Goal: Ensure error is raised when accessing an incorrect MinIO bucket.
Expected Result: Raises "Bucket not found" exception.
Link Here


7. Special Characters in Filename
Name: test_upload_profile_picture_special_characters
Goal: Confirm support for filenames like profile@pic#$.jpg.
Expected Result: Upload successful; URL reflects original filename.
Link Here

8. Simulated Server Error During Upload
Name: test_upload_profile_picture_server_error
Goal: Mimic server failure (e.g., timeout, crash) during upload.
Expected Result: Exception raised with "Server error" message.
Link Here

9. Timeout During URL Generation
Name: test_get_profile_picture_url_timeout
Goal: Handle long response times gracefully during URL retrieval.
Expected Result: Raises exception: "Request timed out".
Link Here

10. Upload of an Empty File
Name: test_upload_profile_picture_empty_file
Goal: Test behavior with a 0-byte file.
Expected Result: File uploads successfully and returns a valid URL.
Link Here

Overall Impact
These test cases not only enhanced the reliability and resilience of the profile picture upload system but also bolstered the integrity of the MinIO integration. From backend robustness to edge-case coverage, the testing effort ensured the feature is both production-ready and maintainable.


# Feature:- Profile Picture Upload via MinIO Integration
To enhance the user experience and personalization within the user management system, a robust profile picture upload feature was implemented. Leveraging MinIO, a high-performance distributed object storage system, this feature enables users to securely upload and retrieve their profile pictures. It adds a visually engaging and personal dimension to user profiles while ensuring efficiency, scalability, and clean integration with existing APIs.

Implementation Details
API Endpoint for Uploading Images
Developed a dedicated POST endpoint specifically for handling profile picture uploads.
The endpoint validates:
Image format (Supports: .jpeg, .png, .gif)
File size (Limited to 5MB to ensure fast and efficient uploads)
MinIO Integration
Configured MinIO within the system using Docker to handle object storage.
Each uploaded file is assigned a unique key, preventing filename collisions or overwrites.
Images are uploaded using MinIO's Python SDK, and presigned URLs are generated for controlled access.
User Model Enhancement
The user schema was extended to include a field for the profile picture URL.
Existing API responses were updated to include this field, ensuring front-end compatibility.
Image Retrieval Logic
When a user's profile is fetched, the system:
Checks if a custom profile image exists.
Returns a presigned URL from MinIO for secure, temporary access.
Falls back to a default placeholder image if no upload is present.


# Testing & Validation Strategy

Unit Tests: Covered all critical paths—file validation, upload success, and retrieval logic.
Integration Tests: Simulated real user flows to verify the full pipeline from file upload to profile rendering.
Tests ensure:
Invalid files (unsupported types or oversized uploads) are gracefully rejected.
Accurate error messaging enhances usability.
The feature remains stable under expected usage conditions.

Key Considerations
Security: MinIO access is tightly controlled via credentials; HTTPS is used for secure communication.
Validation: Strong input validation ensures only supported files are stored.
Performance: Optimizations such as optional image resizing and buffering improve load times and minimize bandwidth.
Scalability: Built to handle large volumes of requests and file uploads without performance degradation.
Fallback Strategy: Defaults to a generic profile image when no picture is uploaded—ensuring visual consistency.

Key Validation Benefits
Guarantees only valid content is processed and stored.
Prevents storage bloat from unsupported or oversized files.
Enhances reliability and UX by delivering clear, actionable error messages.
Promotes maintainability and confidence with high test coverage.

Step-by-Step Setup
MinIO with Docker
From your project root, run:
docker-compose up
Install Dependencies
pip install minio fastapi uvicorn python-multipart
Initialize MinIO Client
Create and configure a MinIO client to connect and check for bucket availability.
Create Upload Endpoint
Implement an endpoint like /upload-profile-picture/ that:
Accepts image files via multipart/form-data
Stores the image in MinIO's demo bucket
Returns a direct or presigned URL to access the uploaded image
Update User Schema
Add a profile_picture_url field in the User model and schema.
Extend User APIs
Include the new image URL in relevant endpoints like GET /me and PUT /update-profile.
Presigned URL Retrieval
Generate time-limited URLs for image access to prevent unauthorized use.

Expected Output
After running the implementation and uploading a .jpeg file via the provided endpoint, the image will be stored in the MinIO demo bucket and retrievable through a secure presigned URL—visible both via API response and within the MinIO web console.





Github: Link
Docker: Link
