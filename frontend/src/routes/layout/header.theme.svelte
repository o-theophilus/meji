<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	const submit = async () => {
		$user.setting.theme = $user.setting.theme == 'light' ? 'dark' : 'light';

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}/setting`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ theme: $user.setting.theme })
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
			<div class="switch" class:dark={$user.setting.theme == 'dark'}>
				<div>☼</div>
				<div>☾</div>
			</div>
		</div>
	</button>
{/if}

<style>
	button {
		border: none;
		padding: var(--sp2);

		background-color: transparent;
		color: var(--ac2);
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
		background-color: var(--ac4);
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
