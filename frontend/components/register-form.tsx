import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { AuthUtils } from '@/api/auth-utils';
import { useTranslations } from 'next-intl';

export function RegisterForm({ className, ...props }: React.ComponentProps<'div'>) {
    const t = useTranslations('RegisterForm');

    const { register } = AuthUtils;

    const router = useRouter();

    const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.target as HTMLFormElement);
        const username = formData.get('username') as string;
        const email = formData.get('email') as string;
        const password = formData.get('password') as string;
        register(email, username, password)
            .json((json) => {
                console.log(json);
                router.push('/login');
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
                    <form onSubmit={handleRegister}>
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
                                <Label htmlFor="email">{t('email')}</Label>
                                <Input
                                    id="email"
                                    name="email"
                                    type="email"
                                    placeholder="m@example.com"
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
                            <div className="grid gap-3">
                                {/* TODO: Check if password and confirm password are the same */}
                                <Label htmlFor="confirm-password">{t('confirmPassword')}</Label>
                                <Input
                                    id="confirm-password"
                                    type="password"
                                    placeholder={t('confirmPassword')}
                                    required
                                />
                            </div>
                            <div className="flex flex-col gap-3">
                                <Button type="submit" className="w-full">
                                    {t('register')}
                                </Button>
                            </div>
                        </div>
                        <div className="mt-4 text-center text-sm">
                            {t('alreadyHaveAccount')}{' '}
                            <Link href="/login" className="underline underline-offset-4">
                                {t('login')}
                            </Link>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
