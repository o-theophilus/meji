<script>
	import { Button } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Card } from '$lib/layout';
	import { Datetime, Icon } from '$lib/macro';
	import { module } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import Receiver from '../../orders/[slug]/_page.receiver.svelte';
	import EditForm from './form.edit.svelte';
	import PrevForm from './form.prev.svelte';

	let { ops = $bindable(), previous_receivers } = $props();
	let name = 'Receiver';
</script>

<Card
	--card-background-color="var(--bg3_)"
	open={ops.status == name}
	onclick={() => {
		ops.status = ops.status != name ? name : null;
	}}
>
	{#snippet title()}
		<div class="line space" id={name}>
			<div class="title">{name}</div>
			{#if ops.status != name && ops.has_receiver}
				<div class="c">
					<div class="a">Delivery Fee</div>
					<div class="b" transition:slide>
						₦{Number(ops.cart.delivery_cost).toLocaleString()}
					</div>
				</div>
			{/if}
		</div>
	{/snippet}

	{#if !ops.has_receiver}
		<PageNote>
			<Icon icon="User" size="50" />
			No receiver
		</PageNote>
	{:else}
		<div class="card">
			<Receiver receiver={ops.cart.receiver} />
		</div>

		<br />
		<div class="delivery">
			<span class="bold"> Estimated Delivery Date: </span>
			<Datetime datetime={ops.delivery_date} type="date_numeric" />
		</div>
	{/if}

	<br />
	<div class="line">
		<Button
			icon="square-pen"
			onclick={() => {
				ops.error = {};
				module.open(EditForm, { ops });
			}}
		>
			Edit
		</Button>
		{#if previous_receivers.length}
			<Button
				icon="history"
				onclick={() => {
					ops.error = {};
					module.open(PrevForm, { ops, previous_receivers });
				}}
			>
				history
			</Button>
		{/if}
	</div>

	{#if ops.has_receiver}
		<div class="line space total">
			<span class="a">Delivery Fee</span>
			<div class="b">
				₦{Number(ops.cart.delivery_cost).toLocaleString()}
			</div>
		</div>
	{/if}
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

	.delivery {
		font-size: 0.8rem;
		& .bold {
			font-weight: 800;
		}
	}
</style>
