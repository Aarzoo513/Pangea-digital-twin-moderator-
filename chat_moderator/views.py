import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from src.query import run_pangea_pipeline
from .models import SystemPromptConfig
from src.run_groq import get_default_policy


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


@csrf_exempt
def api_get_prompt(request):
    """Get the current system prompt for Groq moderation"""
    if request.method != "GET":
        return JsonResponse({"error": "Only GET is allowed."}, status=405)
    
    try:
        config = SystemPromptConfig.objects.get(name="groq_moderation_prompt")
        prompt_text = config.prompt_text
    except SystemPromptConfig.DoesNotExist:
        # Return default policy if no custom one exists
        prompt_text = get_default_policy()
    
    return JsonResponse({
        "prompt": prompt_text,
        "is_custom": SystemPromptConfig.objects.filter(name="groq_moderation_prompt").exists()
    })


@csrf_exempt
def api_update_prompt(request):
    """Update the system prompt for Groq moderation"""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST is allowed."}, status=405)
    
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)
    
    new_prompt = data.get("prompt", "").strip()
    if not new_prompt:
        return JsonResponse({"error": "Prompt cannot be empty."}, status=400)
    
    # Update or create the configuration
    config, created = SystemPromptConfig.objects.update_or_create(
        name="groq_moderation_prompt",
        defaults={"prompt_text": new_prompt}
    )
    
    return JsonResponse({
        "success": True,
        "message": "System prompt updated successfully",
        "created": created
    })


@csrf_exempt
def api_reset_prompt(request):
    """Reset the system prompt to default by deleting custom configuration"""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST is allowed."}, status=405)
    
    try:
        # Delete custom configuration if it exists
        SystemPromptConfig.objects.filter(name="groq_moderation_prompt").delete()
        return JsonResponse({
            "success": True,
            "message": "Prompt reset to default successfully"
        })
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

