<script>
	import { page } from '$app/state';
	import { app, module } from '$lib/store.svelte.js';
	import { Icon, Avatar } from '$lib/macro';
	import { Login } from '$lib/auth';

	let active = $derived(`@${app.user.username}` == page.url.pathname.split('/')[1]);
</script>

{#if app.login}
	<a class:active href="/@{app.user.username}" data-sveltekit-preload-data>
		<Avatar name={app.user.name} photo={app.user.photo} size="24" --avatar-border-radius="40%" />
		Profile
	</a>
{:else}
	<button onclick={() => module.open(Login)}>
		<Icon icon="user" size="24" />
		Login
	</button>
{/if}

<style>
	button {
		all: unset;
		cursor: pointer;
	}

	a,
	button {
		position: relative;

		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 4px;

		width: 100%;
		height: 100%;
		border-radius: 8px;

		color: var(--ft2);
		fill: var(--ft2);
		font-size: 0.8rem;
		text-decoration: none;
		line-height: 100%;

		transition:
			border-color 0.2s ease-in-out,
			color 0.2s ease-in-out,
			fill 0.2s ease-in-out,
			font-weight 0.2s ease-in-out,
			background-color 0.2s ease-in-out;

		&:hover {
			background-color: var(--bg1);
		}
	}

	.active {
		font-weight: 600;
		color: var(--ft1);
		fill: var(--ft1);
		background-color: var(--bg2);
	}
</style>
