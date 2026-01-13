<script>
	import { module } from '$lib/store.svelte.js';
	import { Content } from '$lib/layout';
	import { Button, RoundButton } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Icon } from '$lib/macro';
	import Form from './form.svelte';
	import Next from '../next.svelte';
	import Receiver from '../../orders/[slug]/_receiver.svelte';

	let { ops = $bindable() } = $props();
</script>

<Content --content-padding-top="1px" --content-background-color="var(--bg2)">
	<div class="line">
		<RoundButton
			icon="arrow-left"
			onclick={() => {
				ops.status = 'cart';
			}}
		></RoundButton>
		<div class="page_title">Cart / Receiver</div>
	</div>

	{#if !ops.isFilled()}
		<PageNote>
			<Icon icon="User" size="50" />
			No receiver
		</PageNote>
	{:else}
		<div class="card">
			<Receiver receiver={ops.cart.receiver} />
		</div>
	{/if}

	<br />
	<Button icon="square-pen" onclick={() => module.open(Form, ops)}>Edit</Button>
</Content>

{#if ops.isFilled()}
	<Next
		value={ops.cart.cost_delivery}
		label="Delivery Cost:"
		btn_label="Next"
		icon2="send-horizontal"
		onclick={() => {
			ops.status = 'pay';
		}}
	></Next>
{/if}

<style>
	.page_title {
		margin: 24px 0;
	}

	.card {
		padding: 16px;
		border-radius: 8px;
		background-color: var(--bg1);
	}
</style>
