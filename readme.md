# Bra Fitting Recommendation System - Technical Assessment

## Introduction
This is a simplified version of a bra fitting recommendation system that helps women find their perfect fit. The system uses RAG (Retrieval Augmented Generation) principles to match user measurements and issues with the most relevant recommendations.

## Time Expectation
Expected completion time: 2-4 hours
Please don't spend more than 4 hours on this task

## Setup Instructions
Prerequisites
Python 3.7+
Node.js 14+
npm/yarn
Backend Setup
BASH

# Create and activate virtual environment
```python -m venv venv```

# Windows
```.\venv\Scripts\activate```

# Mac/Linux
```source venv/bin/activate```

# Install dependencies
```
cd backend
pip install -r requirements.txt
```

# Run backend
```
uvicorn app.main:app --reload
Frontend Setup
BASH
```

# In the frontend directory
```
cd frontend
npm install
npm start
```

The application will be running at:
```
Frontend: http://localhost:3000
Backend: http://localhost:8000
```

## Tasks to Complete
1. Backend Issues
Location: backend/app/recommender.py

Current issues:

Simplistic similarity calculation in calculate_fit_similarity
Basic measurement extraction logic
Generic error handling
Missing input validation
Hardcoded default recommendations
Required improvements:

Implement better similarity matching for measurements and fit issues
Add proper measurement extraction and validation
Add specific error handling
Implement sister size recommendations
2. Frontend Issues
Location: frontend/src/components/ChatInterface.js

# Current issues:

- Missing loading states
- Basic error handling
- Simple recommendation display
- No input validation
- Required improvements:

- Add loading indicators
- Enhance recommendation display
- Add measurement input validation
- Testing Your Changes

# Example Queries
```
"I measure 34 underbust and 38 bust, straps keep falling off"
"My band rides up and I'm measuring 32 under, 37 over"
"36 underbust, 42 bust, getting quadraboob effect"
```

# Expected Improvements
- Better accuracy in size recommendations
- Meaningful confidence scores
- Clear error messages
- Improved user experience

# Evaluation Criteria
- Code Quality (40%)
- Clean, readable code
- Proper error handling
- Meaningful commit messages

  
# Technical Implementation (40%)
- RAG implementation understanding
- Frontend/Backend integration
- Debugging approach
- Edge case handling

# User Experience (20%)
- Interface improvements
- Error feedback
- Loading states

# Submission Instructions
- Fork this repository
- Make your changes
- Submit a pull request with:

## Summary of Changes

- **Backend:**  
  - Enhanced measurement extraction and validation (regex, range checks).
  - Improved similarity calculation (weighted measurements + fit issues).
  - Custom exceptions and user-friendly error handling.
  - No hardcoded defaults; clear message if no match.
  - Sister size recommendations implemented.
  - Comprehensive API tests using pytest.

- **Frontend:**  
  - Added loading spinner and minimum delay for better UX.
  - Enhanced recommendation display (labels, grouping, styled card).
  - Clear error message display.
  - Input validation and user guidance.
  - "Clear" button to reset chat.
  - Automated UI tests using Jest and React Testing Library.

## Reasoning Behind Implementation Choices

- **Separation of concerns:**  
  Each commit addresses a specific feature, I have started with loading sppiner which is quick 
  and easy to do. After that I moved to the backend part more specifically the measurements function.
  Continued with the error handling and testing script. Frontend was left at the very end because 
  there was nothing challenging at this stage.
- **User experience:**  
  Loading states, error messages, and user guidance ensure clarity and usability.
- **Robustness:**  
  Comprehensive validation and error handling prevent crashes and guide users to correct input.
- **Test coverage:**  
  Automated tests ensure reliability and make future changes safe.

## Instructions for Testing Your Changes

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

### Manual Testing

1. Start the backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
2. Start the frontend:
   ```bash
   cd frontend
   npm start
   ```
3. Enter example queries in the chat interface and observe recommendations, confidence, reasoning, fit tips, and error handling.

## Notes for Candidates

- Focus on code quality and maintainability
- Document any assumptions you make
- Consider edge cases in your implementation
- Don't hesitate to ask clarifying questions
- Remember the 4-hour time limit

Good luck! We're looking forward to seeing your implementation.
