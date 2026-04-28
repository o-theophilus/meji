<script>
	import { Icon } from '$lib/macro';

	// TODO: get whatsapp
	// get facebook username
	// thread account
	let platforms = [
		{ icon: 'whatsapp', href: 'https://wa.me/2347077033699/?text=Hello%20Meji' },
		{ icon: 'twitter', href: 'https://x.com/shop_meji_ng' },
		{ icon: 'facebook', href: 'https://web.facebook.com/profile.php?id=61587524220060' },
		{ icon: 'instagram', href: 'https://www.instagram.com/shop_meji_ng/' },
		{ icon: 'youtube', href: 'https://www.youtube.com/@shop_meji_ng/' }
	];
</script>

<div class="line">
	{#each platforms as { icon, href }}
		<a {href} target="_blank" rel="noopener noreferrer">
			<Icon {icon} />
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
