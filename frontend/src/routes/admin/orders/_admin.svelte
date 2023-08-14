<script>
	import { user, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';

	import Ordered_Email from './_ordered_email_template.svelte';
	import Delivered_Email from './_delivered_email_template.svelte';
	let ordered_email;
	let delivered_email;

	export let order;
	let error;

	const submit = async (status) => {
		error = '';
		let mail_content = '';
		if (status == 'next') {
			if (order.status == 'ordered') {
				mail_content = ordered_email.innerHTML;
			}
			if (order.status == 'enroute') {
				mail_content = delivered_email.innerHTML;
			}
		}

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}order_status/${order.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ status, mail_content })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.order);
			} else {
				error = resp.message;
			}
		}
	};

	let status = ['pending', 'ordered', 'processing', 'enroute', 'delivered'];
</script>

<Card>
	<b>
		Admin
	</b>
	<p>
		{#each status as state}
			<span class:active={state == order.status}>
				{state}
			</span>
		{/each}
		<span class="cancelled" class:active={'cancelled' == order.status}> cancelled </span>
	</p>

	<div class="h">
		{#if !['pending', 'ordered'].includes(order.status)}
			<Button
				name="< Prev"
				on:click={() => {
					submit('previous');
				}}
			/>
		{/if}

		{#if !['pending', 'delivered'].includes(order.status)}
			<Button
				name="Next >"
				on:click={() => {
					submit('next');
				}}
			/>
		{/if}
	</div>

	{#if error}
		<p class="error">
			{error}
		</p>
	{/if}

	<Button
		name="Cancel"
		on:click={() => {
			submit('cancelled');
		}}
	/>
	
</Card>

<div style="display: none;">
	<div bind:this={ordered_email}>
		<Ordered_Email {order} user={$user} />
	</div>
	<div bind:this={delivered_email}>
		<Delivered_Email {order} user={$user} />
	</div>
</div>

<style>
	.active {
		color: var(--cl1);
		font-weight: 500;
	}
	.cancelled.active {
		color: var(--cl4);
	}
</style>
