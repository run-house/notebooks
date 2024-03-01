from nbconvert.preprocessors import Preprocessor

class AppendOutputsAsMarkdown(Preprocessor):
    def preprocess(self, notebook, resources):
        executable_cells = []
        for cell in notebook.cells:
            # Add code output to notebook as markdown cells
            # look for { type: 'code', outputs: [ ... { text OR data: { 'text/html' } } ] }
            # convert to {'cell_type': 'markdown', 'metadata': {}, 'source': "..." }
            executable_cells.append(cell)
            if cell.cell_type == 'code':
                for output in cell.get('outputs'):
                    text = output.get('text')
                    if text:
                        # Add additional spacing to break up sections for markdown parsing
                        executable_cells.append({'cell_type': 'raw', 'metadata': {}, 'source': "\n" })
                        executable_cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': f"Out[ ]:\n```\n{text.strip()}\n```" })

                # Add additional spacing to break up sections for markdown parsing
                executable_cells.append({'cell_type': 'raw', 'metadata': {}, 'source': "\n" })

        notebook.cells = executable_cells
        return notebook, resources