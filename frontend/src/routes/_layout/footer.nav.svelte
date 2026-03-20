<script>
	import { Link } from '$lib/button';
</script>

<section>
	<div class="block">
		<div class="title">Quick Links</div>
		<Link href="/">Home</Link>
		<Link href="/#about">About</Link>
		<Link href="/contact">Contact Us</Link>
		<Link href="/contact">Partner</Link>
	</div>
	<div class="block">
		<div class="title">Discover</div>
		<Link href="/">Blog</Link>
		<Link href="/">3D Hub</Link>
		<Link href="/faq">FAQ</Link>
	</div>
	<div class="block">
		<div class="title">Legal</div>
		<Link href="/legal/terms">Terms & Conditions</Link>
		<Link href="/legal/policy">Privacy Policy</Link>
		<Link href="/legal/policy#cookiesPolicy">Cookie Policy</Link>
	</div>
</section>

<style>
	section {
		display: flex;
		gap: 40px;
		flex-wrap: wrap;
	}

	.block {
		display: flex;
		flex-direction: column;
		gap: 4px;
		width: fit-content;

		--link-font-size: 0.8rem;
		--link-color: var(--ft2);
		--link-font-weight: 400;

		& .title {
			color: var(--ft1);
			font-weight: 600;
			margin-bottom: 8px;
		}
	}
</style>
