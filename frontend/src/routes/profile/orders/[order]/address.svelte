<script>
	import { module } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import Form from './address__form.svelte';

	export let order;
	export let previous_recipients;
	$: r = order.recipient;
	$: a = r.address;

	$: complete_address =
		r.name && r.phone && a.line && a.state && a.country && a.local_area && a.postal_code;
</script>

<div class="title">
	<b> Shipping Information </b>
</div>
<span> Recipient: </span>
Name:
{#if r.name}
	{r.name}
{:else}
	No Name
{/if}
<br />
Phone:
{#if r.phone}
	{r.phone}
{:else}
	No Phone
{/if}
<br />
<span> Address: </span>
{#if complete_address}
	{a.line}, {a.local_area} , {a.state} , {a.country} , {a.postal_code}
{:else}
	No Address
{/if}

{#if order.status == 'pending'}
	<Button
		class={!complete_address ? 'primary' : ''}
		icon="edit"
		on:click={() => {
			$module = {
				module: Form,
				data: {
					order,
					previous_recipients
				}
			};
		}}
	/>
{/if}

<style>
	span {
		font-weight: 500;
	}
</style>
