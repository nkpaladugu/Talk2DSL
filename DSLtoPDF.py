from fpdf import FPDF
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
import re

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'DSL File Content', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_code(self, code, lexer_name='text'):
        try:
            lexer = get_lexer_by_name(lexer_name)
        except ClassNotFound:
            lexer = get_lexer_by_name('text')
        formatter = HtmlFormatter()
        highlighted = highlight(code, lexer, formatter)
        # Strip HTML tags for plain text rendering
        text = re.sub(r'<[^>]+>', '', highlighted)
        # Replace multiple newlines with single newline
        text = re.sub(r'\n{2,}', '\n', text)
        self.set_font('Courier', '', 10)
        self.multi_cell(0, 5, text)

def convert_dsl_to_pdf(input_file, output_file, lexer_name='text'):
    try:
        # Read the DSL file
        with open(input_file, 'r', encoding='utf-8') as f:
            dsl_content = f.read()
        
        # Create PDF instance
        pdf = PDF()
        pdf.add_page()
        
        # Add DSL content with optional syntax highlighting
        pdf.add_code(dsl_content, lexer_name)
        
        # Save the PDF
        pdf.output(output_file)
        print(f"Successfully converted {input_file} to {output_file}")
    
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    input_dsl = "input.dsl"
    output_pdf = "output.pdf"
    # Use 'text' lexer for plain text DSL; change to 'python', 'json', etc., if DSL has specific syntax
    convert_dsl_to_pdf(input_dsl, output_pdf, lexer_name='text')
