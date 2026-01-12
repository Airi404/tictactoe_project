import os
from django.shortcuts import render
from .forms import ChatForm
from google import genai

def chat_view(request):
    response_text = None
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            api_key = os.environ.get("GEMINI_API_KEY")
            
            if not api_key:
                response_text = "ERROR: No se detecta la clave. Reinicia VS Code."
            else:
                client = genai.Client(api_key=api_key)
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash", 
                        contents=prompt
                    )
                    response_text = response.text
                except Exception:
                    try:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash", 
                            contents=prompt
                        )
                        response_text = response.text
                    except Exception as e:
                        response_text = f"Error persistente de la API: {e}"
    else:
        form = ChatForm()

    return render(request, 'chatbot/chat.html', {'form': form, 'response': response_text})