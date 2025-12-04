import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from src.query import run_pangea_pipeline


def moderate(request):
    # Serve the HTML/JS UI
    return render(request, "ui.html")


@csrf_exempt  # simplify dev; later you can switch to proper CSRF handling
def api_ask(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST is allowed."}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return JsonResponse({"error": "Prompt cannot be empty."}, status=400)

    # Call the backend pipeline
    result = run_pangea_pipeline(prompt)

    if result.get("status") == "rejected":
        return JsonResponse(
            {
                "error": "prompt_rejected",
                "category": result.get("category"),
                "rationale": result.get("rationale"),
            },
            status=400,
        )

    # Normal successful case
    return JsonResponse(
        {
            "answer1": result.get("answer1", ""),
            "answer2": result.get("answer2", ""),
        }
    )
