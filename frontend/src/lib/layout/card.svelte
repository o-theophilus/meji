<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { FoldButton } from '$lib/button';

	let { open = true, onclick, children, title, border = false } = $props();
</script>

<div class="card" class:open>
	{#if title || onclick}
		<div
			class="title"
			role="presentation"
			onclick={(e) => {
				if (e.target != e.currentTarget) return;
				if (onclick) onclick();
			}}
		>
			<div class="a">
				{@render title?.()}
			</div>

			{#if onclick}
				<FoldButton {open} {onclick} />
			{/if}
		</div>
	{/if}

	{#if open}
		<div
			class="content"
			class:border
			transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}
		>
			{@render children()}
		</div>
	{/if}
</div>

<style>
	.card {
		margin: 8px 0;
		background-color: var(--bg1);
		border-radius: 8px;
	}

	.content {
		padding: 24px;
		padding-top: 0;
	}
	.border {
		padding-top: 24px;
		border-top: 1px solid var(--bg2);
	}

	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 16px;
		padding: 24px;
	}
	.a {
		width: 100%;
		pointer-events: none;
	}
</style>
