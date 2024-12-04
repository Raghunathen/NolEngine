# NolEngine

**NolEngine** is a project designed to generate stories inspired by Christopher Nolan's screenplays. It includes tools for processing, training, and generating text based on screenplay data.

---

## **Features and Tools**

### **1. Text Processing**
- **pdfToText**: Converts screenplay PDFs into plain text for easier processing.
- **merger**: Merges multiple text files into a single consolidated dataset for training.

### **2. Model Architectures**
- **NolEngine1**: Based on Andrej Karpathy's GPT model, adapted for text generation tasks.
- **NolEngine_Claude**: An optimized version of the engine with improvements inspired by Claude.

---

## **Tokenizer**
- **NolEngine.model**: A Byte Pair Encoding (BPE) tokenizer tailored for this project to efficiently tokenize screenplay texts.

---

## **Training**
- **initial_trainer**: The primary training loop implemented on Google Colab for initial experiments.
- **minbpe**: Backend system handling BPE tokenization during training.

---

## **Miscellaneous**
- **a.ipynb**: A rough local notebook used for experimentation and quick testing.

---

## **Workflow**
1. **Convert PDFs to Text**: Use `pdfToText` to preprocess screenplay PDFs.
2. **Merge Datasets**: Use `merger` to combine text files into a cohesive dataset.
3. **Tokenization**: Tokenize the text data using the custom BPE tokenizer (`NolEngine.model`).
4. **Training**: Train the model using `initial_trainer` or `NolEngine1` architecture.
5. **Generate Text**: Use the trained model to create stories, leveraging the optimized pipeline.

---

## **Future Plans**
- Fine-tune the model for better storytelling coherence.
- Expand datasets to include more diverse narrative structures.
- Optimize tokenizer performance and integration.

---

## **Acknowledgments**
- Inspired by **Andrej Karpathy's GPT** architecture for small-scale, efficient language modeling.
- Engine optimizations are enhanced with insights from **Claude**.

--- 

NolEngine is a step towards understanding and recreating the complex narratives characteristic of Nolan's storytelling, leveraging state-of-the-art text generation techniques.
