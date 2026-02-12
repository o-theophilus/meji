<script>
	import { Icon } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';

	const submit = async (theme) => {
		if (app.user.theme == theme) return;
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

{#if app.user}
	<div class="radio">
		<button onclick={() => submit('system')} class:active={app.user.theme == 'system'}>
			<Icon icon="laptop" />
		</button>
		<button onclick={() => submit('light')} class:active={app.user.theme == 'light'}>
			<Icon icon="sun" />
		</button>
		<button onclick={() => submit('dark')} class:active={app.user.theme == 'dark'}>
			<Icon icon="moon" />
		</button>
	</div>
{/if}

<style>
	.radio {
		display: flex;
		position: relative;
		z-index: 0;

		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);

		outline: 1px solid var(--ol);
		outline-offset: 1px;
		border-radius: 12px;
	}

	button {
		all: unset;
		cursor: pointer;

		display: flex;
		justify-content: center;
		align-items: center;

		width: 24px;
		aspect-ratio: 1;
		border-radius: 50%;
		background-color: transparent;

		&::before {
			content: '';
			position-anchor: --active;
			z-index: -1;

			position: absolute;
			top: anchor(top);
			bottom: anchor(bottom);
			right: anchor(right);
			left: anchor(left);

			background-color: hsl(0, 0%, 5%);
			border-radius: 50%;

			transition:
				top 0.2s ease-in-out,
				bottom 0.2s ease-in-out,
				right 0.2s ease-in-out,
				left 0.2s ease-in-out;
		}

		&.active {
			color: hsl(0, 0%, 95%);
			anchor-name: --active;
		}
	}
</style>
