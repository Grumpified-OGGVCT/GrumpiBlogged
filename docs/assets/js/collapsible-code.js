/**
 * Collapsible Code Blocks for GrumpiBlogged
 * 
 * Automatically wraps long code blocks in collapsible containers
 * Default: shown (expanded)
 * User can collapse/expand as needed
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find all code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach((codeBlock, index) => {
        const pre = codeBlock.parentElement;
        const codeText = codeBlock.textContent;
        const lineCount = codeText.split('\n').length;
        
        // Only make collapsible if more than 15 lines
        if (lineCount > 15) {
            // Create wrapper
            const wrapper = document.createElement('details');
            wrapper.className = 'collapsible-code';
            wrapper.open = true; // Default to shown
            
            // Create summary (header)
            const summary = document.createElement('summary');
            summary.className = 'code-toggle';
            
            // Detect language from class
            const language = codeBlock.className.match(/language-(\w+)/)?.[1] || 'code';
            
            summary.innerHTML = `
                <span class="code-icon">📝</span>
                <span class="code-label">${language.toUpperCase()} Code Example</span>
                <span class="code-lines">(${lineCount} lines)</span>
                <span class="toggle-icon">▼</span>
            `;
            
            // Clone the pre element
            const preClone = pre.cloneNode(true);
            
            // Replace original pre with wrapper
            pre.parentNode.replaceChild(wrapper, pre);
            
            // Add summary and pre to wrapper
            wrapper.appendChild(summary);
            wrapper.appendChild(preClone);
            
            // Add toggle event listener
            wrapper.addEventListener('toggle', function() {
                const icon = this.querySelector('.toggle-icon');
                icon.textContent = this.open ? '▼' : '▶';
            });
        }
    });
    
    console.log(`✅ Collapsible code blocks initialized (${codeBlocks.length} blocks processed)`);
});

