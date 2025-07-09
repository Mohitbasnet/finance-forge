# 💰 Finance Forge

A comprehensive financial management web application built with Django, featuring currency conversion, investment planning, and user profile management.

## 🚀 Features

### 💱 Currency Converter
- Real-time currency conversion between multiple currencies
- Support for GBP, USD, EUR, BRL, JPY, and TRY
- Transaction history tracking
- Save favorite conversion quotes

### 📈 Investment Calculator
- Compound interest calculations
- Multiple investment types (Savings, Stocks, Bonds, etc.)
- Interactive growth charts using Chart.js
- Investment history tracking
- Investment planning tools

### 👤 User Management
- User registration and authentication
- Comprehensive user profiles
- Profile picture upload
- Password management
- Activity tracking

### 📊 Dashboard & Analytics
- Personal dashboard with activity overview
- Transaction history
- Saved quotes management
- Investment history
- User statistics

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js
- **Database**: SQLite (Development)
- **Icons**: Font Awesome

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/finance-forge.git
   cd finance-forge
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   # For production
   pip install -r requirements.txt
   
   # For development (includes testing and formatting tools)
   pip install -r requirements-dev.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser**
   Navigate to `http://127.0.0.1:8000/`

## 📁 Project Structure

```
finance-forge/
├── finance_forge/          # Django project settings
├── currency_converter/     # Main app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Form classes
│   ├── urls.py            # URL patterns
│   └── migrations/        # Database migrations
├── templates/             # HTML templates
│   └── currency_converter/
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
├── media/                # User uploaded files
├── manage.py             # Django management script
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
└── README.md            # Project documentation
```

## 🎯 Key Features Explained

### Currency Conversion
- **Real-time Rates**: Uses mock exchange rates (can be replaced with real API)
- **Transaction Tracking**: Every conversion is logged for authenticated users
- **Quote Saving**: Users can save important conversions with notes

### Investment Planning
- **Compound Interest**: Calculates investment growth over time
- **Visual Charts**: Interactive charts showing investment progression
- **Multiple Types**: Supports various investment vehicles
- **History Tracking**: All calculations are saved for reference

### User Profiles
- **Comprehensive Data**: Personal information, preferences, and bio
- **Profile Pictures**: Upload and manage profile images
- **Activity Overview**: View recent transactions and saved quotes
- **Password Management**: Secure password change functionality

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
The project uses SQLite by default. For production, consider using PostgreSQL or MySQL.

## 🚀 Deployment

### For Production
1. Set `DEBUG = False` in settings.py
2. Configure a production database
3. Set up static file serving
4. Configure media file storage
5. Set up HTTPS
6. Use a production WSGI server (Gunicorn, uWSGI)

### Using Docker (Optional)
```bash
# Build the image
docker build -t finance-forge .

# Run the container
docker run -p 8000:8000 finance-forge
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/Mohitbasnet)
- LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/mohit-basnet-1b963a25a/)

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Chart.js Library
- Font Awesome Icons

## 📞 Support

If you have any questions or need help, please open an issue on GitHub or contact the author.

---

⭐ **Star this repository if you found it helpful!** 