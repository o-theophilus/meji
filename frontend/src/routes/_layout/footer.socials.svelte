<script>
	import { Icon } from '$lib/macro';

	// TODO: get facebook username
	let platforms = [
		{ name: 'whatsapp', href: 'https://wa.me/2347077033699?text=Hello Meji' },
		{ name: 'twitter', href: 'https://x.com/shop_meji_ng' },
		{ name: 'facebook', href: 'https://web.facebook.com/profile.php?id=61587524220060' },
		{ name: 'instagram', href: 'https://www.instagram.com/shop_meji_ng' },
		// { name: 'threads', href: 'https://www.threads.com/@shop_meji_ng' },
		// { name: 'bluesky', href: 'https://shop-meji-ng.bsky.social' },
		{ name: 'youtube', href: 'https://www.youtube.com/@shop_meji_ng' }
	];
</script>

<div class="line">
	{#each platforms as { name, href }}
		<a {href} target="_blank" rel="noopener noreferrer">
			<Icon icon={name} />
		</a>
	{/each}
</div>

<style>
	.line {
		gap: 4px;
	}

	a {
		--size: 32px;
		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
		border-radius: 40%;

		background-color: var(--bg2);
		fill: var(--ft2);
		color: var(--ft2);

		transition: background-color 0.2s ease-in-out;
	}

	a:hover {
		background-color: var(--bg1);
	}
</style>
