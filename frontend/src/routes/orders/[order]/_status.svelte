<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import SVG from '$lib/svg.svelte';
	import Info from '$lib/info.svelte';
	import Email from './email_template_delivered.svelte';
	let email_template;

	let note = 'I approve this';
	let order = { ...$module.order };
	let items = [...$module.items];
	let order_status = [...$module.order_status];
	let index = order_status.indexOf(order.status);
	let error = {};

	const validate = async (status) => {
		error = {};

		if (!note) {
			error.note = 'This field is required';
		}

		Object.keys(error).length === 0 && submit(status);
	};

	const submit = async (status) => {
		error = {};

		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/status/${order.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				status,
				email_template: email_template.innerHTML.replace(/&amp;/g, '&'),
				note
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			let old_status = order.status;
			$portal = {
				type: 'order',
				data: resp.order
			};

			$module = {
				module: Info,
				status: 200,
				title: 'Status Changed',
				message: `
from: **${old_status}**
<br/>
to: **${status}**
				`,
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Change Order Status</b>
	</svelte:fragment>

	{#each order_status as s, i}
		<div class="state row">
			<div class="circle" class:active={i <= index}>
				<SVG type="check" size="10" />
			</div>
			<span class="cap">
				{s}
			</span>
		</div>
	{/each}
	<br />

	<IG name="note" {error} type="textarea" bind:value={note} placeholder="Note here" />

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<div class="row">
		{#if index > 0}
			<Button
				on:click={() => {
					validate(order_status[index - 1]);
				}}
			>
				&lt; Back
			</Button>
		{/if}

		<Button
			primary
			on:click={() => {
				validate(order_status[index + 1]);
			}}
		>
			<span class="cap">
				{order_status[index + 1]} &gt;
			</span>
		</Button>
	</div>
</Form>

<div bind:this={email_template} style="display: none;">
	<Email {order} {items} />
</div>

<style>
	.row {
		display: flex;
		gap: var(--sp1);
	}
	.cap {
		text-transform: capitalize;
	}

	.state {
		align-items: center;
		gap: var(--sp2);
		margin: var(--sp0) 0;
	}

	.circle {
		--size: 24px;

		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
		
		border-radius: 50%;
		background-color: var(--ac4);
		outline: 2px solid var(--ac6);
		outline-offset: -4px;
		fill: var(--ac6_);
	}

	.circle.active {
		background-color: var(--cl5);
	}
</style>
