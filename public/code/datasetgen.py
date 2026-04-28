def create_conversation_batch(profile: dict, count: int) -> ProfilerBatch | None:
    prompt = f"""
    You are generating realistic user chat messages to train a video game chatbot.

    Generate exactly {count} unique messages that all fit this profile:

    - Communication style: {profile['communication_style']}
    - Player type: {profile['player_type']}
    - Writing pattern: {profile['writing_pattern']}
    - Verbosity: {profile['verbosity']}
    """

    response = client.responses.parse(
        model=DATAGEN_MODEL,
        input=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        stream=False,
        text_format=ProfilerBatch
    )

    return response.output_parsed

def generate_dataset(num_examples: int, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        generated = 0
        pbar = tqdm(total=num_examples)
        while generated < num_examples:
            count = min(BATCH_SIZE, num_examples - generated)
            profile = {
                "communication_style": random.choice(COMMUNICATION_STYLES),
                "player_type": random.choice(PLAYER_TYPES),
                "writing_pattern": random.choice(WRITING_PATTERNS),
                "verbosity": random.choices(VERBOSITY, weights=VERBOSITY_WEIGHTS)[0],
            }

            batch_result = None
            while batch_result is None:
                batch_result = create_conversation_batch(profile, count)

            for example in batch_result.examples:
                template = {
                    "message": example.message,
                    "labels": {
                        "communication_style": profile["communication_style"],
                        "player_type": profile["player_type"],
                        "writing_pattern": profile["writing_pattern"],
                        "verbosity": profile["verbosity"]
                    }
                }
                f.write(json.dumps(template, ensure_ascii=False) + "\n")

            generated += count
            pbar.update(count)
            f.flush()

        pbar.close()