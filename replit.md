# Overtime Hours Aggregation App

## Overview

This is a Japanese overtime hours aggregation application built with Streamlit. The app reads employee overtime data from a CSV file and provides functionality to calculate and display overtime statistics per employee. It processes staff numbers, names, regular overtime hours, and late-night overtime hours, converting decimal time values to a human-readable hours:minutes format.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit
- **Layout**: Wide page layout for data display
- **Language**: Japanese UI with Japanese column names and labels

### Data Processing
- **Data Source**: CSV file with CP932 (Japanese Windows) encoding
- **Location**: `attached_assets/過剰残業_1768802890577.csv`
- **Processing Library**: Pandas for data manipulation and aggregation

### Core Features
1. **CSV Loading**: Reads Japanese-encoded CSV files with error handling
2. **Column Detection**: Dynamic column name matching to handle variations in Japanese text (full-width vs half-width characters)
3. **Time Conversion**: Converts decimal hours to hours:minutes format for readability
4. **Data Aggregation**: Groups data by staff number and name, summing overtime values

### Design Decisions
- **Flexible Column Matching**: Uses substring matching for column names to handle encoding variations between full-width and half-width Japanese characters
- **Error Handling**: Graceful error display when file loading fails
- **Null Safety**: Handles NaN values in time conversion function

## External Dependencies

### Python Packages
- **streamlit**: Web application framework for data apps
- **pandas**: Data manipulation and CSV processing

### Data Files
- CSV file containing overtime records with Japanese encoding (CP932)
- Expected columns: Staff number, Name (Kanji), Regular overtime hours, Late-night overtime hours