<script>
	import { slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { app } from '$lib/store.svelte.js';
	import { FoldButton } from '$lib/button';
	import One from './one.svelte';

	let { ops = $bindable() } = $props();
	let name = 'Items';
</script>

<div class="content" id={name}>
	{#if ops.status == name}
		<div class="content" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each app.cart_items as item (item.key + JSON.stringify(item.variation))}
				<div animate:flip={{ delay: 0, duration: 500, easing: cubicInOut }}>
					<One {item} bind:ops />
				</div>
			{/each}
		</div>
	{/if}

	<div
		class="total line space"
		onclick={() => {
			ops.status = ops.status != name ? name : null;
		}}
		role="presentation"
	>
		<div class="title">{name}</div>

		<div class="line d">
			<div class="c">
				<div class="a">Total Amount</div>
				<div class="b">
					₦{ops.total_items().toLocaleString()}
				</div>
			</div>
			<FoldButton open={ops.status == name} onclick={() => {}} />
		</div>
	</div>
</div>

<style>
	.content {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.total {
		background-color: var(--bg);
		padding: 24px 16px;
		border-radius: 8px;
	}
	.title {
		font-size: 1.2rem;
	}

	.d {
		gap: 16px;
	}
	.c {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
	}
	.a {
		font-size: 0.8rem;
	}
	.b {
		font-weight: bold;
		font-size: 1.2rem;
		color: var(--ft1);
	}
</style>
