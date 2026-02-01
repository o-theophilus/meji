<script>
	import { Link } from '$lib/button';
</script>

<section>
	<div class="block">
		<div class="title">Quick Links</div>
		<Link --link-font-size="0.8rem" href="/">Home</Link>
		<Link --link-font-size="0.8rem" href="/#about">About</Link>
		<Link --link-font-size="0.8rem" href="/contact">Contact Us</Link>
	</div>
	<div class="block">
		<div class="title">Quick Links</div>
		<Link --link-font-size="0.8rem" href="/">Home</Link>
		<Link --link-font-size="0.8rem" href="/#about">About</Link>
		<Link --link-font-size="0.8rem" href="/contact">Contact Us</Link>
	</div>
	<div class="block">
		<div class="title">Legal</div>
		<Link --link-font-size="0.8rem" href="/terms">Terms</Link>
		<Link --link-font-size="0.8rem" href="/privacy">Privacy Policy</Link>
	</div>
</section>

<style>
	section {
		display: flex;
		justify-content: space-between;
		gap: 40px;
		flex-wrap: wrap;
	}

	.block {
		display: flex;
		flex-direction: column;
		width: fit-content;

		--link-color: var(--ft2);
		--link-font-weight: 400;

		& .title {
			color: var(--ft1);
			font-weight: 600;
			margin-bottom: 12px;
		}
	}
</style>
