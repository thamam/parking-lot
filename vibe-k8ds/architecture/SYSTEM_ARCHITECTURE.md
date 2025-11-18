# System Architecture for Vibe-K8ds

## Architecture Overview

### High-Level System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   iOS App    │  │ Android App  │  │   Web App    │          │
│  │  (React      │  │  (React      │  │  (React)     │          │
│  │   Native)    │  │   Native)    │  │              │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼──────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                         HTTPS/WSS
                             │
┌─────────────────────────────┼──────────────────────────────────┐
│                    API GATEWAY / CDN                            │
│                   (Cloudflare / AWS)                            │
└─────────────────────────────┼──────────────────────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
┌─────────▼──────┐  ┌────────▼────────┐  ┌─────▼──────────┐
│  Application   │  │  Voice Services │  │  Media CDN     │
│   Server       │  │                 │  │  (Static       │
│  (Node.js/     │  │  - Speech-to-   │  │   Assets)      │
│   Express)     │  │    Text         │  │                │
│                │  │  - Text-to-     │  │  - Animations  │
│  - REST API    │  │    Speech       │  │  - Images      │
│  - GraphQL     │  │  - Voice        │  │  - Sounds      │
│  - WebSockets  │  │    Recognition  │  │  - Videos      │
└────────┬───────┘  └─────────────────┘  └────────────────┘
         │
         │
┌────────▼──────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Activity    │  │  Progress    │  │  Adaptive    │        │
│  │  Engine      │  │  Tracker     │  │  Learning    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Analytics   │  │  Parent      │  │  Content     │        │
│  │  Engine      │  │  Dashboard   │  │  Manager     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────┬──────────────────────────────────────────────────────┘
         │
┌────────▼──────────────────────────────────────────────────────┐
│                       DATA LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  PostgreSQL  │  │    Redis     │  │    S3/       │        │
│  │              │  │              │  │  Cloud       │        │
│  │  - User Data │  │  - Sessions  │  │  Storage     │        │
│  │  - Progress  │  │  - Cache     │  │              │        │
│  │  - Analytics │  │  - Real-time │  │  - Media     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└───────────────────────────────────────────────────────────────┘
```

## Technology Stack Recommendations

### Frontend (Cross-Platform)

**Primary Choice: React Native**

**Rationale**:
- Single codebase for iOS and Android
- Native performance (critical for animations)
- Excellent animation libraries (Reanimated 2)
- Large ecosystem and community
- Can share code with web version (React Native Web)

**Core Libraries**:
```javascript
{
  "framework": "React Native 0.74+",
  "stateManagement": "Zustand (lightweight, easy to use)",
  "animations": {
    "primary": "React Native Reanimated 2",
    "secondary": "Lottie for complex animations",
    "particles": "React Native Skia"
  },
  "voice": {
    "speechToText": "@react-native-voice/voice",
    "textToSpeech": "react-native-tts",
    "audioPlayback": "react-native-track-player"
  },
  "gestures": "React Native Gesture Handler",
  "haptics": "react-native-haptic-feedback",
  "sensors": "react-native-sensors",
  "navigation": "React Navigation 6",
  "offline": "WatermelonDB (local-first database)",
  "testing": {
    "unit": "Jest",
    "e2e": "Detox",
    "accessibility": "react-native-accessibility"
  }
}
```

**Alternative: Flutter**
- Pros: Excellent performance, beautiful animations, single codebase
- Cons: Smaller ecosystem, Dart language learning curve
- Use if: Team has Dart expertise

### Backend

**Primary Choice: Node.js with TypeScript**

**Rationale**:
- Same language as frontend (TypeScript)
- Excellent for real-time features (WebSockets)
- Great performance for I/O operations
- Large ecosystem for audio/video processing

**Stack**:
```javascript
{
  "runtime": "Node.js 20 LTS",
  "language": "TypeScript 5+",
  "framework": "Express.js or Fastify",
  "api": {
    "rest": "Express.js + OpenAPI spec",
    "graphql": "Apollo Server (optional)",
    "realtime": "Socket.io or WebSockets"
  },
  "orm": "Prisma (type-safe, great DX)",
  "validation": "Zod",
  "authentication": "Passport.js + JWT",
  "testing": {
    "unit": "Vitest",
    "integration": "Supertest",
    "e2e": "Playwright"
  }
}
```

### Database

**Primary: PostgreSQL**

**Rationale**:
- ACID compliance (data integrity critical for progress tracking)
- JSON support for flexible activity data
- Mature, reliable, well-documented
- Excellent performance

**Schema Design**:
```sql
-- User & Authentication
users (id, email, created_at, last_login)
profiles (user_id, display_name, age, avatar_id, preferences)
parent_accounts (id, email, password_hash, verified)
child_accounts (id, parent_id, profile_data)

-- Progress & Learning
progress (child_id, activity_id, status, attempts, completed_at)
achievements (child_id, badge_id, earned_at)
sessions (child_id, started_at, ended_at, activities_completed)
analytics_events (child_id, event_type, event_data, timestamp)

-- Content
activities (id, world_id, level, content, difficulty)
worlds (id, name, description, unlock_criteria)
assets (id, type, url, metadata)

-- Adaptive Learning
skill_assessments (child_id, skill_type, proficiency_level, updated_at)
recommendations (child_id, activity_id, reason, priority)
```

**Cache Layer: Redis**

**Use Cases**:
- Session management
- Real-time leaderboards (if added later)
- Rate limiting
- Caching frequently accessed data
- Queue for background jobs

### Voice Services

**Speech Recognition (Speech-to-Text)**

**Recommended: Multi-Provider Approach**

1. **Primary: Google Cloud Speech-to-Text (Child-friendly)**
   - Pros: Best accuracy, supports multiple languages, kid-specific models
   - Cons: Cost, requires internet
   - Use for: Primary voice commands

2. **Fallback: On-Device Recognition**
   - iOS: Apple's Speech Framework
   - Android: Android Speech Recognizer
   - Use for: Offline mode, privacy-sensitive scenarios

**Text-to-Speech**

**Recommended: Amazon Polly Neural Voices**

**Rationale**:
- Most natural-sounding voices
- Multiple child-friendly voices
- Multiple languages
- Good pricing
- Low latency with caching

**Architecture**:
```
User taps button
     ↓
Check local cache for audio
     ↓ (if not cached)
Request from Polly API
     ↓
Cache audio file locally
     ↓
Play audio
```

**Alternative: On-Device TTS**
- iOS: AVSpeechSynthesizer
- Android: TextToSpeech
- Use for: Offline mode

### Media & Assets

**Content Delivery Network (CDN)**

**Recommended: Cloudflare CDN**

**Assets Structure**:
```
cdn.vibek8ds.com/
├── animations/
│   ├── characters/
│   │   ├── codey/
│   │   │   ├── idle.json (Lottie)
│   │   │   ├── walk.json
│   │   │   └── celebrate.json
│   ├── effects/
│   │   ├── confetti.json
│   │   └── sparkles.json
├── audio/
│   ├── voice/
│   │   ├── en/
│   │   │   ├── intro_01.mp3
│   │   │   └── celebrate_01.mp3
│   ├── sfx/
│   │   ├── tap.mp3
│   │   ├── success.mp3
│   │   └── error.mp3
│   ├── music/
│   │   └── background_01.mp3
├── images/
│   ├── characters/
│   ├── backgrounds/
│   └── ui/
```

**Optimization**:
- Lottie JSON for animations (small file size, scalable)
- WebP/AVIF for images with PNG fallback
- Compressed audio (AAC/Opus)
- Lazy loading and prefetching strategies

### Analytics & Monitoring

**Analytics Platform**

**Recommended: Mixpanel + Custom Backend**

**Rationale**:
- COPPA compliant (with proper configuration)
- Excellent event tracking
- Funnel and retention analysis
- User property tracking
- Custom backend for sensitive data

**Events to Track**:
```javascript
{
  // User Actions
  "activity_started": { activity_id, world_id, timestamp },
  "activity_completed": { activity_id, time_taken, attempts },
  "command_placed": { command_type, position, activity_id },
  "hint_requested": { activity_id, hint_type },
  "error_made": { activity_id, error_type, command_sequence },

  // Engagement
  "session_started": { timestamp, session_number },
  "session_ended": { duration, activities_count },
  "break_taken": { duration },

  // Voice
  "voice_command_used": { command, recognized, success },
  "tts_played": { text_id, language },

  // Progress
  "level_up": { new_level, world_id },
  "badge_earned": { badge_id, timestamp },

  // Parent
  "parent_dashboard_viewed": { section },
  "settings_changed": { setting, old_value, new_value }
}
```

**Monitoring: Sentry**

- Error tracking and crash reporting
- Performance monitoring
- Real user monitoring (RUM)
- Release tracking

### Adaptive Learning Engine

**Machine Learning Components**

**Skill Assessment Model**:
```python
# Simplified example
def assess_skill_level(child_id, skill_type):
    """
    Analyzes child's performance to determine skill proficiency
    """
    recent_activities = get_recent_activities(child_id, skill_type)

    factors = {
        'completion_rate': calculate_completion_rate(recent_activities),
        'attempts_per_activity': calculate_avg_attempts(recent_activities),
        'time_per_activity': calculate_avg_time(recent_activities),
        'hint_usage': calculate_hint_frequency(recent_activities),
        'error_patterns': analyze_error_patterns(recent_activities)
    }

    proficiency = calculate_weighted_score(factors)
    return proficiency_level(proficiency)  # Beginner, Intermediate, Advanced
```

**Recommendation Engine**:
```python
def recommend_next_activity(child_id):
    """
    Suggests next best activity based on child's profile
    """
    profile = get_child_profile(child_id)
    skill_levels = get_all_skill_levels(child_id)
    completed = get_completed_activities(child_id)
    preferences = analyze_preferences(child_id)

    candidates = filter_available_activities(
        skill_levels,
        completed,
        max_difficulty=profile.age_appropriate_difficulty
    )

    scored_activities = []
    for activity in candidates:
        score = calculate_activity_score(
            activity,
            skill_levels,
            preferences,
            diversity_bonus=True  # Encourage variety
        )
        scored_activities.append((activity, score))

    return sorted(scored_activities, key=lambda x: x[1], reverse=True)[0]
```

**Technology**:
- Python microservice for ML operations
- scikit-learn for simple models
- TensorFlow.js for client-side predictions (future)

### Infrastructure & Deployment

**Recommended: AWS or Google Cloud Platform**

**Architecture**:
```
┌─────────────────────────────────────────────────────┐
│                  PRODUCTION SETUP                    │
└─────────────────────────────────────────────────────┘

┌─────────────────┐     ┌─────────────────┐
│  Cloudflare CDN │────→│  Load Balancer  │
│  (Edge Network) │     │  (AWS ALB/GCP)  │
└─────────────────┘     └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
            ┌───────▼──────┐ ┌──▼────────┐ ┌─▼──────────┐
            │  App Server  │ │App Server │ │ App Server │
            │  (Container) │ │(Container)│ │(Container) │
            └──────────────┘ └───────────┘ └────────────┘
                    │
            ┌───────▼─────────────────┐
            │  Managed Services       │
            ├─────────────────────────┤
            │  - RDS (PostgreSQL)     │
            │  - ElastiCache (Redis)  │
            │  - S3 (Media Storage)   │
            │  - CloudFront (CDN)     │
            └─────────────────────────┘
```

**Container Orchestration**:
- **Development**: Docker Compose
- **Production**: Kubernetes (EKS/GKE) or AWS ECS

**CI/CD Pipeline**:
```yaml
# Example GitHub Actions workflow
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    - run: npm test
    - run: npm run test:e2e
    - run: npm run accessibility-tests

  build:
    - build: docker image
    - push: to container registry

  deploy:
    - staging: auto-deploy
    - production: manual approval required
```

## Security & Privacy

### COPPA Compliance

**Requirements**:
1. **No Personal Info from Children**:
   - No names, emails, photos from child interface
   - Parents provide all PII
   - Child profiles use avatars, not photos

2. **Parental Consent**:
   - Verified email confirmation
   - Clear privacy policy in plain language
   - Opt-in for any data collection

3. **Data Minimization**:
   - Collect only what's necessary
   - Automatic data deletion after inactivity
   - No third-party analytics in child mode

4. **No Ads or Tracking**:
   - Zero advertising
   - No cross-site tracking
   - No cookies in child interface

**Implementation**:
```typescript
// Child data model - pseudonymized
interface ChildProfile {
  id: string;  // UUID, not sequential
  parentId: string;
  pseudonym: string;  // "Red Puppy", "Blue Robot"
  age: number;  // Only age, not DOB
  preferences: {
    avatarId: string;
    voiceId: string;
    language: string;
  };
  // NO: name, photo, email, location
}

// All analytics pseudonymized
interface AnalyticsEvent {
  childPseudoId: string;  // Hashed, rotated monthly
  eventType: string;
  eventData: object;
  timestamp: number;
  // NO: IP address, device ID, geolocation
}
```

### Data Encryption

**At Rest**:
- Database: Encryption at rest (AWS RDS encryption)
- File storage: Server-side encryption (S3)
- Sensitive fields: Application-level encryption (AES-256)

**In Transit**:
- HTTPS/TLS 1.3 for all communications
- Certificate pinning in mobile apps
- WebSocket Secure (WSS)

**Secrets Management**:
- AWS Secrets Manager or GCP Secret Manager
- Never commit secrets to code
- Rotate credentials regularly

### Authentication & Authorization

**Parent Authentication**:
```typescript
// JWT-based authentication
interface ParentAuthToken {
  userId: string;
  email: string;
  role: 'parent';
  iat: number;
  exp: number;  // 7 days
}

// Refresh token for long-term sessions
interface RefreshToken {
  tokenId: string;
  userId: string;
  expiresAt: Date;  // 90 days
}
```

**Child "Authentication"**:
```typescript
// No passwords for kids - visual selection
interface ChildSession {
  childId: string;
  parentId: string;
  deviceId: string;
  createdAt: Date;
  // Auto-expires after 24 hours
}

// Child selects their avatar to "log in"
// Parent can enable PIN if desired
```

**Access Control**:
- Parents can only access their children's data
- Children can only access age-appropriate content
- API endpoints have role-based access control

## Performance Requirements

### Latency Targets

**User Interactions**:
- Touch response: <50ms (imperceptible delay)
- Command execution: <100ms
- Voice recognition: <500ms
- Screen transition: <200ms
- Animation start: <16ms (60fps)

**API Response Times**:
- GET requests: <200ms (p95)
- POST requests: <500ms (p95)
- Analytics events: Fire-and-forget (async)

**Media Loading**:
- Initial app load: <3 seconds
- Activity load: <1 second
- Audio playback: <200ms from trigger
- Image load: Progressive (show immediately)

### Offline Support

**Offline-First Architecture**:
```typescript
// Local-first data flow
User Action
     ↓
Update Local DB (WatermelonDB)
     ↓
Update UI immediately
     ↓
Queue sync to backend
     ↓
Sync when online
```

**Offline Capabilities**:
- ✅ Play downloaded activities
- ✅ Track progress locally
- ✅ Voice commands (on-device)
- ✅ Save creations
- ❌ Sync across devices (requires internet)
- ❌ Parent dashboard (requires internet)

**Content Prefetching**:
- Download next 3 activities in advance
- Preload audio for upcoming sessions
- Cache animations for current world

## Scalability Considerations

### Initial Scale (MVP)

**Expected Load**:
- 10,000 registered users
- 1,000 daily active users
- 50 concurrent users (peak)

**Infrastructure**:
- 2-3 app servers (auto-scaling)
- 1 database instance (db.t3.medium)
- 1 Redis instance (cache.t3.small)
- CDN for media

### Growth Scale (Year 1)

**Expected Load**:
- 100,000 registered users
- 10,000 daily active users
- 500 concurrent users (peak)

**Infrastructure**:
- 5-10 app servers (auto-scaling)
- Database read replicas
- Larger Redis instance
- Dedicated analytics pipeline

### Bottlenecks to Watch

1. **Voice Recognition API costs** (can spike)
   - Solution: Implement caching, on-device fallback

2. **Database writes** (analytics events)
   - Solution: Batch writes, use time-series DB

3. **Media bandwidth**
   - Solution: CDN, progressive loading, compression

## Development Phases

### Phase 1: MVP (3-4 months)
- Core app framework
- World 1 (5 activities)
- Basic voice interaction
- Parent dashboard (basic)
- iOS + Android

### Phase 2: Enhancement (2-3 months)
- World 2-3
- Improved adaptive learning
- Better analytics
- Web version

### Phase 3: Scale (2-3 months)
- World 4
- Multi-language support
- Advanced parent features
- Performance optimization

---

**Next Document**: Frontend Architecture Details
