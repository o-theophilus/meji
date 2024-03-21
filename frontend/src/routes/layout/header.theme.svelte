<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import SVG from '$lib/svg.svelte';

	const submit = async () => {
		$user.setting_theme = $user.setting_theme == 'light' ? 'dark' : 'light';

		await fetch(`${import.meta.env.VITE_BACKEND}/user/setting`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ theme: $user.setting_theme })
		});
	};
</script>

{#if $user}
	<button
		on:keydown
		on:click={() => {
			submit();
		}}
	>
		<div class="block">
			<div class="switch" class:dark={$user.setting_theme == 'dark'}>
				<div>
					<SVG type="light" size="12" />
				</div>
				<div>
					<SVG type="dark" size="12" />
				</div>
			</div>
		</div>
	</button>
{/if}

<style>
	button {
		border: none;
		padding: var(--sp2);

		background-color: transparent;
		fill: var(--ac2);
		cursor: pointer;
	}
	.block {
		--size: 20px;
		position: relative;
		overflow: hidden;

		height: var(--size);
		width: var(--size);

		border-radius: 50%;
	}
	.block:hover {
		fill: var(--ac1);
		background-color: var(--ac5);
	}

	.switch {
		position: absolute;
		top: 0;

		transition: var(--trans1);
	}
	.dark {
		top: -100%;
	}
	.switch div {
		width: var(--size);
		height: var(--size);

		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
