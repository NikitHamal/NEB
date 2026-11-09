# ioe-drive
A collaborative platform for IOE (Institute of Engineering, Nepal) students to share and access academic resources including books, notes, past questions, and study materials organized by semester and subjects.

## Overview
IOE Drive is designed to facilitate the sharing of academic resources among IOE students. It provides a centralized repository where students can upload and access study materials categorized by semester, subjects and departments. The platform aims to enhance the learning experience by making it easier for students to find relevant resources for their courses.

## Architecture
- Architecture Style: Client-Server
- Frontend: Next.js 16 with App Router
- Backend: Node.js with NestJS
- Server Architecture: Layered architecture (Controller → Service → Repository)
- Database: PostgreSQL with Drizzle ORM
- Authentication: Clerk
- Deployment: Vercel (Client), Render (Server)

## Tech Stack
### Frontend
- Next.js 16 with App Router
- Tailwind CSS for styling
- Clerk for authentication
- TanStack Query for server state management
- Lucide React for icons
- Zod and React Hook Form for form validation

### Backend
- NestJS on Node.js
- PostgreSQL with Drizzle ORM
- Clerk for authentication
- Multer for file uploads
- class-validator/class-transformer for schema validation

## Project Structure
```
ioe-drive/
├── .github/
│   └── workflows/
│
├── apps/
│   ├── server/                      # Backend application (NestJS)
│   │   ├── src/
│   │   │   ├── clerk/
│   │   │   ├── common/
│   │   │   │   ├── decorators/
│   │   │   │   ├── dto/
│   │   │   │   ├── filters/
│   │   │   │   ├── guards/
│   │   │   │   ├── interceptors/
│   │   │   │   └── utils/
│   │   │   ├── config/
│   │   │   ├── database/
│   │   │   │   ├── migrations/
│   │   │   │   └── seeders/
│   │   │   ├── modules/
│   │   │   │   ├── health/
│   │   │   │   ├── me/
│   │   │   │   ├── programs/
│   │   │   │   ├── resources/
│   │   │   │   ├── subjects/
│   │   │   │   ├── users/
│   │   │   │   └── webhooks/
│   │   │   ├── storage/
│   │   │   ├── app.module.ts
│   │   │   └── main.ts
│   │   ├── Dockerfile
│   │   └── package.json
│   │
│   └── web/                         # Frontend application
│       ├── public/
│       ├── src/
│       │   ├── app/
│       │   ├── components/
│       │   │   ├── common/
│       │   │   ├── forms/
│       │   │   ├── layout/
│       │   │   └── ui/
│       │   ├── constants/
│       │   ├── context/
│       │   ├── hooks/
│       │   ├── lib/
│       │   │   ├── api/
│       │   │   └── validators/
│       │   ├── providers/
│       │   ├── types/
│       │   └── utils/
│       ├── Dockerfile
│       └── package.json
│
├── docs/
├── docker-compose.yml
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── SETUP.md
```

## Contributing
Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.