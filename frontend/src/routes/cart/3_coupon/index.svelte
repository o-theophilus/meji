<script>
	import { slide } from 'svelte/transition';
	import { module } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';
	import { Card } from '$lib/layout';
	import { Datetime } from '$lib/macro';
	import Form from './form.svelte';

	let { ops = $bindable() } = $props();

	let name = 'Coupons';
</script>

<Card
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

	<span class="label bold"> Delivery Date: </span>
	<span class="label">
		<Datetime datetime={ops.delivery_date} type="date_numeric" />
	</span>
	<!-- {ops.cart.delivery_date} -->

	<br />
	<br />

	<div>
		{#each ops.coupons as cop}
			<div class="line space">
				<div class="a">
					{cop.code} -
					{#if cop.type == 'number'}₦{/if}{cop.value}{#if cop.type == 'percent'}%{/if}
					off {cop.entity}
				</div>

				<div class="b">
					{#if cop.entity == 'items'}
						{#if cop.type == 'number'}
							₦{cop.value.toLocaleString()}
						{:else if cop.type == 'percent'}
							₦{((ops.total_items() * cop.value) / 100).toLocaleString()}
						{/if}
					{:else if cop.entity == 'delivery'}
						{#if cop.type == 'number'}
							₦{cop.value.toLocaleString()}
						{:else if cop.type == 'percent'}
							₦{((Number(ops.cart.cost_delivery) * cop.value) / 100).toLocaleString()}
						{/if}
					{/if}
				</div>
			</div>
		{/each}
	</div>

	<br />
	<Button icon="square-pen" onclick={() => module.open(Form, ops)}>Add Coupon</Button>

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
		border-top: 1px solid var(--bg2);
	}

	.label {
		font-size: 0.8rem;
	}
	.bold {
		font-weight: 800;
	}
</style>
