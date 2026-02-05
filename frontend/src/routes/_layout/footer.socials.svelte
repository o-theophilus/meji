<script>
	import { Icon } from '$lib/macro';
	import { BackButton } from '$lib/button';

	// TODO: get whatsapp
	// get facebook username
	// thread account
	let platforms = [
		{ icon: 'whatsapp', href: 'https://wa.me/2348067397793/?text=Hello%20Theophilus' },
		{ icon: 'twitter', href: 'https://x.com/shop_meji_ng' },
		// { icon: 'github', href: 'https://github.com/o-theophilus' },
		// { icon: "discord", href: 'https://discord.com/users/theophilus#6682' },
		{ icon: 'facebook', href: 'https://web.facebook.com/profile.php?id=61587524220060' },
		{ icon: 'instagram', href: 'https://www.instagram.com/shop_meji_ng/' },
		// { icon: 'linkedin', href: 'https://www.linkedin.com/in/o-theophilus/' },
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

		transition:
			background-color 0.2s ease-in-out,
			fill 0.2s ease-in-out,
			color 0.2s ease-in-out;
	}

	a:hover {
		background-color: var(--cl1);
		fill: white;
		color: white;
	}
</style>
