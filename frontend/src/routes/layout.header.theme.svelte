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
	<section
		on:keydown
		on:click={() => {
			submit();
		}}
	>
		<div class="block">
			<div class="switch" class:dark={$user.setting.theme == 'dark'}>
				<div class="state">☼</div>
				<div class="state">☾</div>
			</div>
		</div>
	</section>
{/if}

<style>
	section {
		color: var(--font2);
		cursor: pointer;

		padding: var(--gap2);
	}
	.block {
		--size: 20px;
		position: relative;
		overflow: hidden;

		height: var(--size);
		width: var(--size);
	}
	.switch {
		position: absolute;
		top: 0;

		transition: var(--trans1);
	}
	.dark {
		top: -100%;
	}
	.state {
		width: var(--size);
		height: var(--size);

		border-radius: 50%;

		display: flex;
		justify-content: center;
		align-items: center;

		background-color: var(--background);
	}
</style>
