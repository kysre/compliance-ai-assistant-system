import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import Link from 'next/link';
import { AuthUtils } from '@/api/auth-utils';
import { useRouter } from 'next/navigation';
import { useTranslations } from 'next-intl';

export function LoginForm({ className, ...props }: React.ComponentProps<'div'>) {
    const t = useTranslations('LoginForm');

    const { login, setAuthToken, setAuthUser } = AuthUtils;

    const router = useRouter();

    const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.target as HTMLFormElement);
        const username = formData.get('username') as string;
        const password = formData.get('password') as string;
        login(username, password)
            .json((json) => {
                setAuthToken(json.token);
                console.log(json.user);
                setAuthUser(json.user);
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
                    <CardTitle>{t('title')}</CardTitle>
                    <CardDescription>{t('description')}</CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleLogin}>
                        <div className="flex flex-col gap-6">
                            <div className="grid gap-3">
                                <Label htmlFor="username">{t('username')}</Label>
                                <Input
                                    id="username"
                                    name="username"
                                    type="text"
                                    placeholder={t('username')}
                                    required
                                />
                            </div>
                            <div className="grid gap-3">
                                <div className="flex items-center">
                                    <Label htmlFor="password">{t('password')}</Label>
                                </div>
                                <Input
                                    id="password"
                                    name="password"
                                    type="password"
                                    placeholder={t('password')}
                                    required
                                />
                            </div>
                            <div className="flex flex-col gap-3">
                                <Button type="submit" className="w-full">
                                    {t('login')}
                                </Button>
                            </div>
                        </div>
                        <div className="mt-4 text-center text-sm">
                            {t('noAccount')}{' '}
                            <Link href="/register" className="underline underline-offset-4">
                                {t('register')}
                            </Link>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
