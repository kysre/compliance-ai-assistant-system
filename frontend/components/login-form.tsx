import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import Link from 'next/link';
import { AuthUtils } from '@/api/auth-utils';
import { useRouter } from 'next/navigation';

export function LoginForm({ className, ...props }: React.ComponentProps<'div'>) {
    const { login, setAuthToken } = AuthUtils;

    const router = useRouter();

    const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.target as HTMLFormElement);
        const username = formData.get('username') as string;
        const password = formData.get('password') as string;
        login(username, password)
            .json((json) => {
                setAuthToken(json.token);
                console.log(json);
                router.push('/');
            })
            .catch((err) => {
                // TODO: Add error handling (Show toast)
                console.error(err);
            });
    };

    return (
        <div className={cn('flex flex-col gap-6', className)} {...props}>
            <Card>
                <CardHeader>
                    <CardTitle>Login to your account</CardTitle>
                    <CardDescription>
                        Enter your username and password below to login to your account
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleLogin}>
                        <div className="flex flex-col gap-6">
                            <div className="grid gap-3">
                                <Label htmlFor="username">Username</Label>
                                <Input
                                    id="username"
                                    name="username"
                                    type="text"
                                    placeholder="username"
                                    required
                                />
                            </div>
                            <div className="grid gap-3">
                                <div className="flex items-center">
                                    <Label htmlFor="password">Password</Label>
                                    {/* TODO: Add forgot password link */}
                                    <a
                                        href="#"
                                        className="ml-auto inline-block text-sm underline-offset-4 hover:underline"
                                    >
                                        Forgot your password?
                                    </a>
                                </div>
                                <Input id="password" name="password" type="password" required />
                            </div>
                            <div className="flex flex-col gap-3">
                                <Button type="submit" className="w-full">
                                    Login
                                </Button>
                            </div>
                        </div>
                        <div className="mt-4 text-center text-sm">
                            Don&apos;t have an account?{' '}
                            <Link href="/register" className="underline underline-offset-4">
                                Register
                            </Link>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
