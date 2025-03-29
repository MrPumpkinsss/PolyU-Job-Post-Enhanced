# Job-Post-Enhanced

**Job-Post-Enhanced** is a web project that crawls a school's job board website, gathers job posting data, and then enhances the global search functionality. The improved results are presented on my own website: [https://mrpumpkinsss.github.io/Job-Post-Enhanced/](https://mrpumpkinsss.github.io/Job-Post-Enhanced/).

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Running](#setup-and-running)
- [Disclaimer](#disclaimer)
- [Dependencies and Resources](#dependencies-and-resources)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project extracts job posting information from the school’s job board using a web crawler. After enhancing the search functionality with multi-keyword search, case sensitivity options, and sortable columns, the data is displayed in a user-friendly interface built using HTML, CSS, and JavaScript. The Excel file (`job_listings.xlsx`) generated from the crawler is parsed on the client side using the [SheetJS XLSX](https://github.com/SheetJS/sheetjs) library.

## Features

- **Data Collection**  
  Crawls the school’s job board site and collects job postings, storing the information in an Excel file (`job_listings.xlsx`).

- **Global Search**  
  Provides two search fields that support live filtering of job listings. Users can choose to enable case sensitivity in their searches.

- **Job Type Filtering**  
  Offers a dropdown menu to filter job postings by type (e.g., Graduate Position, Part-time Position, Temporary Position, etc.).

- **Sortable Data**  
  The summary table supports sorting by columns like "Recruitment ID", "Post Date", and "Deadline". Clicking the relevant header toggles between ascending and descending order.

- **Data Display**  
  - **Left Panel:** Displays a summary of job postings, combining company name, position, salary, and job type into one column along with additional details like Recruitment ID, Post Date, and Deadline.  
  - **Right Panel:** When a summary row is clicked, detailed job information (HTML formatted) is shown. The content is sanitized by removing any images and certain SVG icons.

- **Disclaimer Modal**  
  On initial load, a disclaimer modal informs users about the data source, the potential for data delays or inaccuracies, and limits of liabilities. Users must acknowledge this disclaimer by clicking the "Agree" button before using the site.

## Project Structure

```
Job-Post-Enhanced/
├── index.html          # Main webpage containing HTML, CSS, and JavaScript
├── job_listings.xlsx   # Excel file containing crawled job data
└── README.md           # Project documentation file
```

- **index.html**  
  The entire interface is built within this file. It includes the layout for disclaimer, filtering options, left/right panels for data display, and integration with the SheetJS library for parsing Excel data.

- **job_listings.xlsx**  
  This file contains the job data fetched by the web crawler. JavaScript fetches and parses this file to generate a dynamic job listing table on the page.

## Setup and Running

### Local Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/mrpumpkinsss/Job-Post-Enhanced.git
   cd Job-Post-Enhanced
   ```

2. **Dependencies:**  
   The project primarily relies on front-end resources, including the SheetJS XLSX library via a CDN, so no additional installation is required.

3. **Launch a Local Server:**  
   It is recommended to run the project on a local HTTP server. You can use tools like the Live Server extension in VSCode or the following command with [http-server](https://www.npmjs.com/package/http-server):

   ```bash
   # Using http-server
   npx http-server
   ```

4. **Access the Project:**  
   Open your browser and navigate to the provided URL (e.g., `http://localhost:8080`) to view the website.

### Deployment on GitHub Pages

1. Push the code to your GitHub repository.
2. In the repository settings, activate GitHub Pages using either the `main` or `gh-pages` branch.
3. After configuration, the site will be available at `https://mrpumpkinsss.github.io/Job-Post-Enhanced/`.

## Disclaimer

> **Disclaimer:**  
> The information presented on this website is collected via web crawling from the school's job board (e.g., PolyU POSS) and is not directly provided by the original job posting institution.  
> - The data may have delays or inaccuracies and is intended for reference only.  
> - Users are advised to verify the original data or contact the publisher before making any decisions.  
> - Neither the website nor its operators accept any liability for errors or delays in the information presented.  
> - Any discrepancies due to updates on third-party websites are not the responsibility of this website.

Users must click the “Agree” button on the disclaimer modal upon load to proceed.

## Dependencies and Resources

- **SheetJS XLSX Library**  
  The library is loaded through the CDN: [https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js](https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js)

- **Google Fonts**  
  The project uses the Roboto font family, loaded from: [https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap](https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap)

- **Browser APIs**  
  Utilizes the Fetch API to retrieve the Excel file and standard DOM manipulation for dynamic content rendering.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to open an issue or submit a pull request.

## License

This project is open-source and distributed under the [MIT License](LICENSE).
