private string BuildSystemPrompt()
{
    return $@"You are a chatbot. Adapt your tone to match this player profile. Your only job is to talk to the player. Do not use any special characters.

            Player profile scores: {_playerProfile.ToPromptSummary()}
            Dominant style: {_playerProfile.DominantType()}

            Adjust your response length, formality, and energy to suit this player. Do NOT provide anything besides messages.";
}

public async Task SendMessageAsync(string userText)
{
    var profilerResult = await ProfilerService.Instance.ClassifyAsync(userText);
    _playerProfile.Update(profilerResult);
    Debug.Log($"Profile: {_playerProfile.ToPromptSummary()} | Dominant: {_playerProfile.DominantType()}");
    
    var systemPrompt = BuildSystemPrompt();
    
    var response = await OpenRouterService.Instance.ChatAsync(systemPrompt, userText);

    if (response != null)
        _chatUI.AddMessage(new ChatMessage("Model", response));
    
    _debugUI.Refresh(_playerProfile, profilerResult, response);
}
    
