async function saveNotes() {
    const notes = document.getElementById('notes').value;

    const response = await fetch('/api/save_notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes: notes })
    });

    const data = await response.json();
    alert(data.message);
}

async function askQuestion() {
    const question = document.getElementById('question').value;
    const notes = document.getElementById('notes').value;

    const response = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question, context: notes })
    });

    const data = await response.json();
    const responseDiv = document.getElementById('response');
    responseDiv.innerText = data.response;

    // Adjust the response box size
    responseDiv.style.height = '300px';
}
