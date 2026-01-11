 Amharic Information Retrieval Project
 
 Group Project
This project was developed as part of a **collaborative coursework initiative** at Addis Ababa University. Team members contributed across multiple areas including web crawling, data preprocessing, statistical analysis, vector space modeling, and GUI development. My role focused primarily on **UI improvements, documentation, testing, and team coordination**. All contributions are traceable and part of the shared project repository.

 Introduction
This project is an Amharic information retrieval system that consists of the following components:

- **Web Spider**: Downloads Amharic files from the internet.
- **PDF to Image Conversion**: Converts the downloaded PDF files containing text into images.
- **Text Operations**: Extracts and processes text from images, including tokenization, punctuation removal, normalization, and stemming.
- **Statistical Analysis**: Analyzes processed text to verify Zipf's law and Luhn's law.
- **Inverted Index**: Creates an inverted index from the processed text.
- **Vector Space Model**: Uses the inverted index to build a vector space model employing cosine similarity for information retrieval.
- **Search Engine GUI**: Provides a user interface linking queries to the relevant websites where the resources were found.

Usage
- **Web Crawling**: The web spider component downloads Amharic files from the internet, expanding the corpus.
- **PDF to Image Conversion**: Processes the downloaded PDF files, converting them to images for text extraction.
- **Text Processing**: Extracted text is tokenized, punctuation is removed, then normalized and stemmed, followed by statistical analysis.
- **Inverted Index Creation**: Processed text is used to create an inverted index, forming the foundation of the information retrieval system.
- **Vector Space Model**: The inverted index is used to create a vector space model, employing cosine similarity for retrieval.
- **Search Engine GUI**: Users can search for relevant documents using the GUI. Queries link to the relevant websites where the resources were found.

My Contributions
My contributions focused on **user interface, usability, and non-code support** for the project. Specifically, I:

- Improved the **Search Engine GUI** by refining labels, button placement, and sidebar toggle behavior for better usability.
- Enhanced the **stacked pages** (Results, Tokenization, Stemmer, Normalize) with clearer labels and Amharic placeholder texts.
- Synchronized **sidebar and top buttons** to ensure consistent toggling between minimized and full sidebar views.
- Made **minor visual improvements** such as spacing, icon sizes, and modern fonts to improve readability and user experience.
- Assisted in **testing and verifying** that the UI changes did not affect the underlying information retrieval logic.
- Contributed to **documentation and README updates**, making instructions clear and user-friendly.
- Helped **organize the dataset and example files** for demonstration and testing purposes.
- Provided **feedback on workflow and usability**, improving the overall functionality and DEAI alignment of the system.
- Participated in **team coordination**, helping plan UI changes and ensuring consistency across the GUI pages.

These contributions highlight my **non-code and UI-focused involvement**, while ensuring that all changes are traceable in the project history.

Installation and Setup
1. Clone the repository:  
```bash
git clone https://github.com/your-username/amharic-information-retrieval.git
Configure the necessary settings, such as the web crawling parameters and file storage locations.

Run the web crawler, text processing, and information retrieval components.

Start the search engine GUI.

Example

While searching for ፍቅር እስከ መቃብር, the result will appear as shown below. Clicking a result in the GUI will take you to the original website.

Contributions

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to create a new issue or submit a pull request.

License

This project is licensed under the MIT License.