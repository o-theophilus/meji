<script>
	import { Button } from '$lib/button';
	import { Card } from '$lib/layout';
	import { module } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import Add from './_add.svelte';
	import Remove from './_remove.svelte';

	let { ops = $bindable() } = $props();
	console.log(ops.coupon?.benefit);

	let name = 'Coupons';
</script>

<Card
	--card-background-color="var(--bg3_)"
	open={ops.status == name}
	onclick={() => {
		ops.status = ops.status != name ? name : null;
	}}
>
	{#snippet title()}
		<div class="line space">
			<div class="title">{name}</div>
			{#if ops.status != name}
				<div class="c">
					<div class="a">Total Discount</div>
					<div class="b" transition:slide>
						₦{ops.total_items().toLocaleString()}
					</div>
				</div>
			{/if}
		</div>
	{/snippet}

	{#if ops.coupon}
		<div class="line space">
			<div class="a">
				{@html ops.coupon.note}
			</div>

			<div class="b">
				{#if ops.coupon.entity == 'items'}
					{#if ops.coupon.type == 'number'}
						₦{ops.coupon.value.toLocaleString()}
					{:else if ops.coupon.type == 'percent'}
						₦{((ops.total_items() * ops.coupon.value) / 100).toLocaleString()}
					{/if}
				{:else if ops.coupon.entity == 'delivery'}
					{#if ops.coupon.type == 'number'}
						₦{ops.coupon.value.toLocaleString()}
					{:else if ops.coupon.type == 'percent'}
						₦{((Number(ops.cart.cost_delivery) * ops.coupon.value) / 100).toLocaleString()}
					{/if}
				{/if}
			</div>
		</div>
	{/if}

	<br />

	{#if ops.coupon}
		<Button icon="trash-2" onclick={() => module.open(Remove, { ops })}>Remove Coupon</Button>
	{:else}
		<Button icon="square-pen" onclick={() => module.open(Add, { ops })}>Add Coupon</Button>
	{/if}

	<div class="line space total">
		<span class="a">Total Discount</span>
		<div class="b">
			₦{ops.total_items().toLocaleString()}
		</div>
	</div>
</Card>

<style>
	.title {
		font-size: 1.2rem;
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
	.total {
		margin-top: 16px;
		padding-top: 16px;
		border-top: 1px solid var(--bg1);
	}
</style>
