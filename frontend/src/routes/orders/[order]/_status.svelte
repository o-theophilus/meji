<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
	import SVG from '$lib/svg.svelte';
	import Info from '$lib/info.svelte';
	import Email_Processing from './email_template_processing.svelte';
	import Email_Delivered from './email_template_delivered.svelte';
	let email_template;

	let note = 'I approve this';
	let order = { ...$module.order };
	let status = ['ordered', 'processing', 'enroute', 'delivered'];
	let index = status.indexOf(order.status);
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

		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order_status/${order.key}`, {
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
			$portal = resp.order;

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

	{#each status as s}
		<div class="state" class:active={order.status == s}>
			<div class="h">
				<div>
					<div>
						<SVG type="check" />
					</div>
				</div>
				{s}
			</div>
		</div>
	{/each}
	<br />

	<IG name="Note" {error} let:id>
		<textarea bind:value={note} {id} placeholder="Note here" />
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<div class="line">
		{#if index > 0}
			<Button
				on:click={() => {
					validate(status[index - 1]);
				}}
			>
				&lt; Back
			</Button>
		{/if}

		<Button
			class="primary"
			on:click={() => {
				validate(status[index + 1]);
			}}
		>
			<span class="cap">
				{status[index + 1]} &gt;
			</span>
		</Button>
	</div>
</Form>

<div bind:this={email_template} style="display: none;">
	{#if order.status == 'ordered'}
		<Email_Processing {order} />
	{:else if order.status == 'enroute'}
		<Email_Delivered {order} />
	{/if}
</div>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}

	.state {
		--color: var(--cl5);
		--size: 24px;
		text-transform: capitalize;
		fill: var(--ac5_);
	}
	.active ~ .state {
		--color: var(--ac4);
	}

	.h {
		display: flex;
		align-items: center;
		gap: var(--sp2);
		margin: var(--sp0) 0;
	}
	.h div {
		display: flex;
		justify-content: center;
		align-items: center;

		border: 2px solid var(--color);
		border-radius: 50%;
		width: var(--size);
		height: var(--size);
	}
	.h div div {
		width: calc(var(--size) - 8px);
		height: calc(var(--size) - 8px);
		border-radius: 50%;
		background-color: var(--color);
	}

	.cap {
		text-transform: capitalize;
	}
</style>
