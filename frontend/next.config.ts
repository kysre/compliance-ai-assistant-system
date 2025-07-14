import type { NextConfig } from 'next';
import createNextIntlPlugin from 'next-intl/plugin';

const nextConfig: NextConfig = {
    output: 'standalone',
    typescript: {
        ignoreBuildErrors: true, // TODO: Fix typescript type-check errors & remove this
    },
};

const withNextIntl = createNextIntlPlugin();
export default withNextIntl(nextConfig);
