# Voice Interaction Design for Vibe-K8ds

## Voice Design Philosophy

For pre-literate children, voice is the **primary communication channel**. Our voice interface must be:

- **Clear**: Simple words, clear pronunciation
- **Patient**: Never rushed, allows response time
- **Encouraging**: Positive tone, celebrates effort
- **Consistent**: Same character voice throughout
- **Adaptive**: Adjusts to child's pace and understanding

## Voice Character: Codey the Robot

### Character Profile

**Personality**:
- Friendly and enthusiastic
- Patient and understanding
- Playful but not silly
- Encouraging without being patronizing
- Gender-neutral

**Voice Characteristics**:
- **Pitch**: Mid-range (neither too high nor too low)
- **Speed**: 20% slower than adult conversation
- **Tone**: Warm, animated, expressive
- **Energy**: Moderate-high (engaging but not overwhelming)

**Age**: Sounds like a friendly 8-10 year old (relatable peer)

### Voice Selection

**Primary Voice (English)**:
- **Recommended**: Amazon Polly Neural - "Justin" (Child voice)
- **Alternative**: Google Cloud TTS - "Wavenet-J" with slower rate

**Other Languages**:
- Spanish: Polly Neural - "Miguel" (Child)
- French: Polly Neural - "Léa" (Child)
- Mandarin: Google Cloud - Wavenet-B (adjusted pitch)

### Voice Acting Guidelines

When generating or recording voice lines:

```
❌ AVOID:
"Hello there! My name is Codey and I am going to teach you coding today!"
(Too formal, too many words, intimidating)

✅ BETTER:
"Hi! I'm Codey! Want to play?"
(Short, friendly, inviting)

---

❌ AVOID:
"You need to select the forward command and place it in the sequence builder"
(Complex vocabulary, technical terms)

✅ BETTER:
"Can you tap the arrow? Good! Now put it right here."
(Simple words, one step at a time)

---

❌ AVOID:
"Incorrect. Please try again."
(Negative, discouraging)

✅ BETTER:
"Oops! That's okay! Everyone makes mistakes. Let's try together!"
(Positive, normalizes errors, offers support)
```

## Voice Interaction Patterns

### 1. Onboarding & First Time Use

```
[App opens, Codey appears with wave animation]

CODEY: "Hi friend! I'm Codey!"
[Pause 1.5 seconds]

CODEY: "I'm a robot who loves to play!"
[Pause 1.5 seconds]

CODEY: "Can you tap me?"
[Visual: Codey pulses/glows]
[Wait for tap]

CHILD: [Taps]

CODEY: "Yay! You did it!"
[Celebration animation]
[Pause 1 second]

CODEY: "I need your help with something..."
[Pause 1 second]

CODEY: "Can you help me get to that star?"
[Star appears and sparkles]
[Pause 2 seconds - let child observe]

CODEY: "Tap the blue arrow to help me move!"
[Arrow button highlights and pulses]
```

**Key Principles**:
- One sentence at a time
- Pause between sentences (1-2 seconds)
- Wait for child's response (5-10 seconds)
- Visual reinforcement of every instruction

### 2. Activity Introduction

```
[New activity starts]

CODEY: "Wow! Look at this!"
[Show environment - park, playground, etc.]
[Pause 2 seconds]

CODEY: "See that puppy?"
[Puppy appears and barks]
[Pause 1.5 seconds]

CODEY: "He lost his ball!"
[Sad puppy animation]
[Pause 1.5 seconds]

CODEY: "Can you help him find it?"
[Ball sparkles in distance]
[Pause 2 seconds]

CODEY: "Let's use these arrows to walk there!"
[Show command options]
```

**Structure**:
1. Hook attention (exciting discovery)
2. Establish context (who needs help)
3. Define problem (what's wrong)
4. State goal (what we're trying to do)
5. Introduce tools (how to solve it)

### 3. Giving Instructions

**Graduated Prompting**:

```
LEVEL 1 - First Attempt (Full Guidance):
CODEY: "Tap the green arrow. It points this way!"
[Arrow highlights, direction shows]
[Wait 5 seconds]

If no action:
LEVEL 2 - Second Prompt (More Specific):
CODEY: "The green one right here!"
[Arrow pulses rapidly]
[Visual hand points to it]
[Wait 5 seconds]

If still no action:
LEVEL 3 - Direct Show:
CODEY: "Let me show you!"
[Auto-tap animation shows exactly where]
CODEY: "Now you try!"
[Reset and wait 10 seconds]

If action taken at any level:
CODEY: "Yes! Perfect! You got it!"
```

**Instruction Templates**:

```javascript
// Simple action
"Tap the [COLOR] [OBJECT]"
"Drag the [OBJECT] over here"
"Touch the [CHARACTER]"

// Sequence building
"Put the arrow here, in this box"
"Now add another one next to it"
"One more! You're doing great!"

// Execution
"Ready to see what happens?"
"Let's try it! Tap the GO button!"
"Watch this!"
```

### 4. Feedback During Execution

```
[Child places commands and taps GO]

CODEY: "Here I go!"
[Starts executing first command]

[After each command]:
CODEY: "Step!" or "Jump!" or "Turn!"
[Action-specific sound effect]

[On successful completion]:
CODEY: "We did it! We found the ball!"
[Celebration animation]
CODEY: "The puppy is so happy!"
[Puppy wags tail, plays]
CODEY: "You're such a good helper!"

[If sequence doesn't reach goal]:
CODEY: "Hmm, we ended up over here!"
[Show where they ended up]
CODEY: "We need to get over there!"
[Show goal again]
CODEY: "Want to try again? You can do it!"
```

**Execution Commentary**:
- Narrate each action as it happens
- Create cause-effect connection
- Build anticipation
- Celebrate outcome regardless

### 5. Error Handling & Recovery

**First Error** (Encouraging):
```
CODEY: "Oops! That didn't work the way we wanted!"
[Pause 1 second]
CODEY: "But that's okay! That's how we learn!"
[Pause 1 second]
CODEY: "Let's try something different!"
```

**Second Error** (Supportive):
```
CODEY: "Hmm, not quite yet!"
[Pause 1 second]
CODEY: "This one is tricky! Even I get confused sometimes!"
[Pause 1 second]
CODEY: "Want me to give you a hint?"
[Pause 2 seconds, wait for response]
```

**Third Error** (Intervening):
```
CODEY: "You know what? Let's try this together!"
[Pause 1 second]
CODEY: "Watch what I do..."
[Demonstration mode]
[Pause 1 second]
CODEY: "Now you try! I know you can do it!"
```

**Frustration Detected** (Redirecting):
```
CODEY: "Hey! Want to try something else that's really fun?"
[Pause 1 second]
CODEY: "We can come back to this one later!"
[Pause 1 second]
CODEY: "Let's go play over here!"
[Redirect to easier or different activity]
```

### 6. Celebrating Success

**Micro-Celebrations** (After each step):
```
"Nice!"
"Good job!"
"You got it!"
"Perfect!"
"Awesome!"
"Yes!"
```

**Medium Celebrations** (After challenge):
```
CODEY: "You did it! You're amazing!"
[Confetti animation]
CODEY: "That was so cool!"
[Star award animation]
CODEY: "High five!"
[Hand appears for tap]
```

**Big Celebrations** (After level/world):
```
CODEY: "WOW! You finished the whole thing!"
[Big celebration animation]
CODEY: "You are such a good coder!"
[Pause 1 second]
CODEY: "Look what you earned!"
[Badge reveal animation]
[Pause 2 seconds - admire badge]
CODEY: "I'm so proud of you!"
[Codey does happy dance]
```

**Celebration Vocabulary** (Variety is key):
```
Tier 1 (Quick): "Nice!" "Great!" "Yes!" "Good!" "Yay!"
Tier 2 (Medium): "Awesome!" "You did it!" "Perfect!" "Amazing!" "Fantastic!"
Tier 3 (Big): "You're incredible!" "That was amazing!" "You're a superstar!"
```

### 7. Session Transitions

**Starting a Session**:
```
RETURNING USER:
CODEY: "Hey! You're back! I missed you!"
[Codey waves enthusiastically]
[Pause 1 second]
CODEY: "Ready to play?"
[Pause 2 seconds]

DAILY STREAK:
CODEY: "You came back again! That's [NUMBER] days in a row!"
[Show streak counter]
CODEY: "You're on a roll!"
```

**Ending a Session**:
```
NATURAL END (Completed activities):
CODEY: "You did so much today! Look at all these stars!"
[Show today's achievements]
[Pause 2 seconds]
CODEY: "Your brain must be tired from all that thinking!"
[Pause 1 second]
CODEY: "Come back tomorrow for more fun!"
[Wave goodbye]

TIME LIMIT REACHED:
CODEY: "Wow, we played a lot today!"
[Pause 1 second]
CODEY: "Time for a break. Your brain needs rest!"
[Pause 1 second]
CODEY: "See you next time!"
[Friendly goodbye wave]
```

**Break Encouragement**:
```
AFTER 15 MINUTES:
CODEY: "Great playing! Want to take a little break?"
[Pause 2 seconds]
CODEY: "Maybe get some water? Or stretch?"
[Show simple stretch animation]
CODEY: "I'll be here when you're ready!"
```

## Voice Commands from Child

### Supported Commands

**Intent Recognition** (Not exact phrase matching):

```
AFFIRMATIVE:
Child says: "Yes", "Yeah", "Uh-huh", "Okay", "Sure", "Yay"
System recognizes: AFFIRMATIVE_INTENT

NEGATIVE:
Child says: "No", "Nope", "Nuh-uh", "Don't want to"
System recognizes: NEGATIVE_INTENT

HELP REQUEST:
Child says: "Help", "I need help", "Can you help me", "I don't know"
System recognizes: HELP_INTENT

REPEAT REQUEST:
Child says: "Again", "One more time", "Do it again", "Say it again"
System recognizes: REPEAT_INTENT

NAVIGATION:
Child says: "Go back", "Home", "Menu", "Different one"
System recognizes: NAVIGATION_INTENT
```

### Voice Command Flow

```
[Child activates microphone by tapping Codey's microphone icon]

CODEY: "I'm listening!"
[Microphone icon glows, audio visualization shows]

[Child speaks: "Help"]

[Speech-to-text processes]
[System recognizes: HELP_INTENT]

CODEY: "Sure! I can help you!"
[Proceeds to demonstration mode]

---

[If speech not recognized clearly]

CODEY: "Hmm, I didn't quite hear that!"
[Pause 1 second]
CODEY: "Can you say it again?"
[Microphone reactivates]

[If still not recognized after 2 tries]

CODEY: "That's okay! You can tap these buttons instead!"
[Show visual options]
```

### Voice Command Best Practices

**Low Pressure**:
- Voice commands always optional
- Visual alternatives always available
- No penalty for not using voice
- Clear visual feedback when listening

**Kid-Friendly Recognition**:
- Accept mispronunciations
- Ignore background noise (siblings, TV)
- Long timeout (5+ seconds of silence)
- Confidence threshold: 60% (vs 85% for adults)

**Privacy First**:
- Voice activated only by explicit tap
- Clear visual indicator when listening
- No always-on listening
- No voice data stored
- Processing on-device when possible

## Multilingual Voice Strategy

### Priority Languages (Phase 1)
1. English (US, UK, Australia)
2. Spanish (Spain, Latin America)
3. Mandarin Chinese
4. French
5. German

### Localization Considerations

**Not Just Translation**:
```
ENGLISH: "Let's give Codey a high-five!"
SPANISH: "¡Chocamos los cinco con Codey!"
(Not literal translation - culturally appropriate gesture)

ENGLISH: "You earned a gold star!"
MANDARIN: "你得到了一个大红花！"
(Red flower is more culturally significant than star)
```

**Cultural Adaptations**:
- Character names may change
- Celebration styles differ
- Color meanings vary
- Gestures and expressions adapt
- Voice tone expectations differ

**Voice Talent Per Language**:
- Native speakers only
- Child voice actors or synthesized child voices
- Cultural consultants review scripts
- User testing with native-speaking children

## Voice Script Structure

### Script Template

```markdown
## Activity: [Activity Name]
**World**: [World Number]
**Target Age**: [4-5 or 5-6]
**Skill**: [Sequencing/Patterns/etc.]

---

### INTRO
**CODEY**: "[First line establishing context]"
*[Pause 1.5s]*
*[Visual: Description of what appears]*

**CODEY**: "[Second line stating problem/goal]"
*[Pause 2s]*
*[Visual: Description of goal highlight]*

---

### INSTRUCTION
**CODEY**: "[Clear, simple instruction]"
*[Wait for user action]*

*[IF NO ACTION after 5s]:*
**CODEY**: "[Repeat with more specificity]"
*[Visual: Additional highlighting]*

---

### EXECUTION
*[Child taps GO button]*
**CODEY**: "[Anticipatory comment]"

*[During each command execution]:*
**SFX**: [Sound effect description]
**CODEY**: "[Optional narration]"

---

### SUCCESS
**CODEY**: "[Immediate celebration]"
*[Pause 1s]*
*[Visual: Celebration animation]*

**CODEY**: "[Elaboration on success]"
*[Pause 1s]*

**CODEY**: "[Transition to next]"

---

### ERROR (if applicable)
**CODEY**: "[Normalizing mistake]"
*[Pause 1s]*

**CODEY**: "[Encouragement to try again]"
```

### Example Complete Script

```markdown
## Activity: Puppy Finds Ball
**World**: 1
**Target Age**: 4-5
**Skill**: Sequencing (2-3 commands)

---

### INTRO
**CODEY**: "Look! A puppy!"
*[Pause 1.5s]*
*[Visual: Puppy appears, barks, wags tail]*

**CODEY**: "Oh no! He lost his ball!"
*[Pause 1s]*
*[Visual: Puppy looks sad, ball sparkles in distance]*

**CODEY**: "Can we help him find it?"
*[Pause 2s]*
*[Visual: Path lights up slightly]*

---

### INSTRUCTION
**CODEY**: "Let's walk this way!"
*[Pause 1s]*
**CODEY**: "Tap the blue arrow two times!"
*[Visual: Right arrow pulses]*
*[Wait for user action - up to 10s]*

*[IF CORRECT - Child taps arrow twice]:*
**CODEY**: "Perfect! Two arrows! Now tap GO!"
*[GO button pulses]*

*[IF WRONG - Child taps wrong arrow or wrong number]:*
**CODEY**: "Hmm, let's try the blue one that points this way!"
*[Visual: Hand points at correct arrow]*

---

### EXECUTION
*[Child taps GO]*
**CODEY**: "Here we go!"

*[Puppy moves right - Step 1]:*
**SFX**: *Paw step sound*
**CODEY**: "Step!"

*[Puppy moves right - Step 2]:*
**SFX**: *Paw step sound*
**CODEY**: "Step!"

*[Puppy reaches ball]:*
**SFX**: *Happy bark, ball bounce*

---

### SUCCESS
**CODEY**: "Yay! You found the ball!"
*[Pause 1s]*
*[Visual: Puppy jumps happily, confetti]*

**CODEY**: "The puppy is so happy! You're a great helper!"
*[Pause 1.5s]*
*[Visual: Star appears]*

**CODEY**: "You earned a star! Ready for more?"
*[Pause 2s]*
*[Visual: Next activity preview or return to map]*
```

## Voice Performance Optimization

### Caching Strategy

```typescript
// Pre-cache common phrases
const CACHED_PHRASES = [
  "Nice!",
  "Good job!",
  "Try again!",
  "You did it!",
  "Amazing!",
  "Perfect!",
  "Let's go!",
  "Here we go!",
  "Watch this!",
  "Oops!"
];

// Pre-cache all activity intro/outro scripts
// Cache per-session dynamic content
// Prefetch next likely phrases
```

### Latency Reduction

```
User Action Trigger
     ↓
Check local cache (10ms)
     ↓ (if hit)
Play immediately

     ↓ (if miss)
Request from CDN (50-200ms)
     ↓
Cache for next time
     ↓
Play
```

**Target**: <200ms from trigger to audio start

---

**Next Steps**:
1. Create complete voice script library for World 1
2. Record/synthesize all audio files
3. Implement voice command recognition system
4. Conduct user testing with target age group
5. Iterate based on comprehension and engagement data
