@echo off
echo ========================================
echo   Test Database Connection
echo ========================================
echo.

cd /d "%~dp0"

echo Testing database connection...
echo.

python -c "from app.core.database import DatabaseConnection; db = DatabaseConnection(); print('✅ Database connection successful!'); results = db.execute_query('SELECT @@VERSION'); print('SQL Server Version:', results[0] if results else 'Unknown')"

if errorlevel 1 (
    echo.
    echo ❌ Database connection FAILED!
    echo.
    echo Troubleshooting:
    echo 1. Check SQL Server is running
    echo 2. Check .env file configuration:
    echo    - DB_SERVER=localhost
    echo    - DB_NAME=dbCDNNLT
    echo    - DB_USER=sa
    echo    - DB_PASSWORD=123456
    echo 3. Check database 'dbCDNNLT' exists
    echo.
) else (
    echo.
    echo ✅ All tests passed!
    echo.
)

pause
