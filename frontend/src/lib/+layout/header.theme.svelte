<script>
	import { app } from '$lib/store.svelte.js';
	import { Icon } from '$lib/macro';
	import { onMount } from 'svelte';

	let media;
	const apply = () => {
		document.documentElement.dataset.theme =
			app.user.theme == 'system' ? (media.matches ? 'dark' : 'light') : app.user.theme;
	};
	onMount(() => {
		media = window.matchMedia('(prefers-color-scheme: dark)');
		media.addEventListener('change', apply);
		return () => media.removeEventListener('change', apply);
	});

	const submit = async (theme) => {
		app.user.theme = theme;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/theme`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ theme })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			app.user = resp.user;
		} else {
			throw new Error('invalid request');
		}
	};
</script>

<!-- PORTFOLIO: UPDATE THEME COMPONENT -->
{#if app.user}
	<button
		title="theme"
		onclick={() => {
			let theme = 'system';
			if (app.user.theme == 'system') {
				theme = 'light';
			} else if (app.user.theme == 'light') {
				theme = 'dark';
			}
			submit(theme);
		}}
	>
		<div class="switch {app.user.theme} test">
			<div class="state">
				<Icon icon="laptop" />
			</div>
			<div class="state">
				<Icon icon="sun" />
			</div>
			<div class="state">
				<Icon icon="moon" />
			</div>
		</div>
	</button>
{/if}

<style>
	button,
	.state {
		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
	}

	button {
		--size: 20px;

		position: relative;
		overflow: hidden;

		color: var(--ft2);
		border-radius: 50%;
		background-color: transparent;
		border: none;
		cursor: pointer;

		transition:
			color var(--trans),
			background-color var(--trans);
	}

	button:hover {
		color: white;
		background-color: var(--cl1);
	}

	.switch {
		position: absolute;
		top: 0;
		transition: top var(--trans);
	}

	.light {
		top: -20px;
	}
	.dark {
		top: -40px;
	}
</style>
