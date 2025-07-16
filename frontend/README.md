
# Frontend - Compliance AI Assistant System

This is the frontend application for the Compliance AI Assistant System, built with Next.js and TypeScript. It provides a modern, responsive web interface for interacting with the compliance AI assistant and managing regulatory compliance processes.

## Tech Stack

- **Framework**: Next.js 15.3.2 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: Radix UI primitives
- **AI Interface**: Assistant UI React components
- **Internationalization**: next-intl with English and Persian support
- **HTTP Client**: Wretch

## Project Structure

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── dashboard/       # Main dashboard interface (Chat, Regulations view, ...)
│   ├── login/           # Login page
│   └── register/        # Register page
├── components/          # Reusable React components
│   ├── assistant-ui/    # AI assistant interface components
│   ├── ui/              # Base UI components
│   └── regulations/     # Compliance-specific components
├── contexts/            # React context providers
├── hooks/               # Custom React hooks
├── i18n/                # Internationalization configuration
├── messages/            # Translation files (en.json, fa.json)
└── api/                 # API integration layer
```

## Key Features

- **AI-Powered Chat Interface**: Interactive compliance assistant powered by LLMs
- **Multi-language Support**: English and Persian localization
- **Modern UI**: Built with Radix UI components and Tailwind CSS
- **Authentication System**: User registration and login functionality
- **Dashboard Interface**: Centralized compliance management dashboard
- **Responsive Design**: Mobile-first approach with theme support
- **Type Safety**: Full TypeScript implementation

## Getting Started

### Prerequisites

- Node.js 22+ (Alpine-based for Docker compatibility)
- pnpm package manager

### Development Setup

1. Install dependencies:

```bash
pnpm install
```

2. Run the development server:

```bash
pnpm run dev
```

The application will be available at `http://localhost:3000` and will automatically redirect to the dashboard.

### Available Scripts

- `pnpm run dev` - Start development server with Turbopack
- `pnpm run build` - Build for production
- `pnpm run start` - Start production server
- `pnpm run lint` - Run ESLint
- `pnpm run format` - Format code with Prettier

## Configuration

The application uses standalone output for optimized containerization and includes internationalization plugin configuration.

## Docker Deployment

The frontend includes a multi-stage Dockerfile optimized for production deployment:

- **Development**: Hot-reloading enabled
- **Production**: Minimal runtime with standalone output

The application runs on port 3000 in production.

## Development Workflow

The project includes:

- Pre-commit hooks with Husky
- Lint-staged for automated code formatting
- ESLint and Prettier configuration for code quality
- TypeScript with build error suppression (temporary)

## Integration

This frontend communicates with the Django backend API to provide a complete compliance management solution as part of the larger Compliance AI Assistant System.

## Notes

The frontend is currently configured with TypeScript build error suppression, which should be addressed by fixing type-check errors in future development. The application supports both English and Persian languages, making it suitable for international compliance requirements. The AI assistant interface is built using specialized React components designed for conversational AI interactions.
