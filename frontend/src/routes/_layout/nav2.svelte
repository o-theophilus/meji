<script>
	import { page } from '$app/state';
	let active = $derived(page.url.pathname);
</script>

<div class="nav">
	<div class="block">
		<a class:active={active == '/'} href="/">Home</a>
		<a class:active={active == '/about'} href="/about">About</a>
		<a class:active={active == '/contact'} href="/contact">Contact Us</a>
		<a class:active={active == '/partner'} href="/partner">Partner</a>
		<a class:active={active == '/blog'} href="/blog">Blog</a>
	</div>
</div>

<style>
	.nav {
		background-color: var(--bg);
		border-bottom: 1px solid var(--ol);

		& .block {
			display: flex;
			align-items: center;

			max-width: var(--mobileWidth);
			margin: auto;
		}

		position: relative;

		&::before {
			content: '';
			position-anchor: --active;

			position: absolute;
			bottom: anchor(bottom);
			right: anchor(right);
			left: anchor(left);
			height: 4px;

			background-color: var(--cl1);
			border-radius: var(--toggle-border-radius, 4px);

			transition:
				right 0.2s ease-in-out,
				left 0.2s ease-in-out;
		}
	}

	a {
		display: flex;
		align-items: center;
		justify-content: center;

		padding: 16px;
		text-decoration: none;
		color: var(--ft2);
		font-size: 0.8rem;

		transition: background-color 0.2s ease-in-out;

		&.active {
			anchor-name: --active;
			color: var(--ft1);
			background-color: var(--bg2);
		}

		&:hover {
			color: var(--ft1);
			background-color: var(--bg1);
		}
	}
</style>
