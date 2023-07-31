<!-- LINK TO TOP -->
<a name="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ChinaiArman/ViveryDataAnalysis">
    <img src="resources\images\logo.png" alt="Logo" width="200">
  </a>
  <h3 align="center">Vivery Data Analysis</h3>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#update-procedure">Update Procedure</a></li>
    <li><a href="#update-history">Update History</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque lacus orci, dignissim sit amet vestibulum a, congue sit amet metus. Sed rhoncus a ante in rutrum. Nam sollicitudin bibendum quam. Cras luctus libero quis aliquet suscipit. Sed in ligula tincidunt, tincidunt tortor ac, placerat ligula. Mauris lacinia consectetur ipsum, non interdum ex bibendum in. Curabitur viverra, dolor eget rutrum consequat, dui metus tincidunt massa, sit amet interdum lacus eros sed lectus.

![Product Name Screen Shot][sample-cover]

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque lacus orci, dignissim sit amet vestibulum a, congue sit amet metus. Sed rhoncus a ante in rutrum. Nam sollicitudin bibendum quam. Cras luctus libero quis aliquet suscipit. Sed in ligula tincidunt, tincidunt tortor ac, placerat ligula. Mauris lacinia consectetur ipsum, non interdum ex bibendum in. Curabitur viverra, dolor eget rutrum consequat, dui metus tincidunt massa, sit amet interdum lacus eros sed lectus.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Below are a set of instructions that will walk you through setting up this repository. The instructions are written for the **Windows Operating system**, but should be near identical for the Mac OS. The only prerequisites are to **have Python installed on your machine and a bulk upload file to analyze.** 

### Installation

1. Clone this repository
   ```sh
   git clone https://github.com/ChinaiArman/ViveryDataAnalysis.git
   ```
2. Install packages
   ```sh
   pip install -r requirements.txt
   pip install git+https://github.com/PyFPDF/fpdf2.git@master
   ```
3. Obtain API Keys
    1. Visit [MapBoxAPI](https://docs.mapbox.com/help/getting-started/access-tokens/) and follow the instructions to claim both a **Public** and **Secret** API Key.
    2. Create a file within the repository called `keys.py`.
    3. Define two variables, `SK` (for the Secret Key), and `PK` (for the Public Key), and assign their appropriate values.
        ```python
        PK = {public key}
        SK = {secret key}
        ```
4. Install Font Family (Windows OS Instructions)
    1. From root directory: `'resources' > 'Roobert Font Suite' > 'TTF'`
    2. Open all TTF files and click **Install**
    3. Navigate from the Windows Operating System folder: `Fonts`
    4. Clear MatPlotLib font cache by deleting the cache file (`fontlist.json`, likely stored in `Users/{user}/.matplotlib`)

### Usage
5. Add a bulk upload file to the working directory
6. To run the Analytics Engine API File:
    ```sh
    python analyticsEngine.py "{path to file from root directory}"
    ```
    - Desired Output:
      * A folder will be created with the name `data_{bulk upload file name}`, containing the directories `csvs`, `images`, and `resources`, as well as the bulk upload file.
      * Within `csvs`, a copy of all dataframes generated will be stored in CSV format.
      * Within `images`, a copy of all graphs generated will be stored in PNG format.
      * Within `resources`, a copy of all generation data will be stored in CSV/JSON format.
7. To run the pdfWizard File:
    ```sh
    python pdfWizard.py "{path to file from root directory}", "{name of network}"
    ```
    - Desired Output:
      * A folder will be created with the name `data_{bulk upload file name}`, containing the directories `csvs`, `images`, and `resources`, as well as the bulk upload file and the **generated report.**
      * Within `csvs`, a copy of all dataframes generated will be stored in CSV format.
      * Within `images`, a copy of all graphs generated will be stored in PNG format.
      * Within `resources`, a copy of all generation data will be stored in CSV/JSON format.

### Common Bug Fixes
- Font Family Error
  ```sh
  findfont: Font family `Roobert Medium` not found
  ```
    1. Navigate to the MatPlotLib font cache file (`fontlist.json`, likely stored in `Users/{user}/.matplotlib`)
    2. Open the file in an IDE (VSCode)
    3. Use `ctrl + F` and search `Roobert`
    4. For each value of `Roobert` under the `name` key, change the name to match the specific font (found at the end of the string under the `fname` key)
        - Before:
          ```json
          {
            "fname": "C:\\Users\\arman\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Roobert-Medium.ttf",
            "name": "Roobert",
            "style": "normal",
            "variant": "normal",
            "weight": 500,
            "stretch": "normal",
            "size": "scalable",
            "__class__": "FontEntry"
          },
          ```
        - After:
          ```json
          {
            "fname": "C:\\Users\\arman\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Roobert-Medium.ttf",
            "name": "Roobert Medium",
            "style": "normal",
            "variant": "normal",
            "weight": 500,
            "stretch": "normal",
            "size": "scalable",
            "__class__": "FontEntry"
          },
          ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Update Procedure

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque lacus orci, dignissim sit amet vestibulum a, congue sit amet metus. Sed rhoncus a ante in rutrum. Nam sollicitudin bibendum quam. Cras luctus libero quis aliquet suscipit. Sed in ligula tincidunt, tincidunt tortor ac, placerat ligula. Mauris lacinia consectetur ipsum, non interdum ex bibendum in. Curabitur viverra, dolor eget rutrum consequat, dui metus tincidunt massa, sit amet interdum lacus eros sed lectus.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- UPDATE HISTORY -->
## Update History

- ``July 1, 2023 --> Begin initial development``
- ``July 27, 2023 --> Release version 1.1.0``

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque lacus orci, dignissim sit amet vestibulum a, congue sit amet metus. Sed rhoncus a ante in rutrum. Nam sollicitudin bibendum quam. Cras luctus libero quis aliquet suscipit. Sed in ligula tincidunt, tincidunt tortor ac, placerat ligula. Mauris lacinia consectetur ipsum, non interdum ex bibendum in. Curabitur viverra, dolor eget rutrum consequat, dui metus tincidunt massa, sit amet interdum lacus eros sed lectus.

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[sample-cover]: resources/images/sample_cover.png
