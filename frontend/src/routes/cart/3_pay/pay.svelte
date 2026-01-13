<script>
	import { goto } from '$app/navigation';
	import { app, module, loading } from '$lib/store.svelte.js';

	import { Button, Link } from '$lib/button';
	import { Dialogue, Note } from '$lib/info';
	import Next from '../next.svelte';

	import Email_Admin from './email_template_admin.svelte';
	import Email_User from './email_template_user.svelte';
	let email_template_admin;
	let email_template_user;

	let { ops, total } = $props();
	let error = $state({});

	const make_payment = async () => {
		error = {};
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/check`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			const paystack = PaystackPop.setup({
				key: import.meta.env.VITE_PAYSTACK_KEY,
				email: app.user.email,
				amount: resp.pay * 100,
				callback: (resp2) => {
					submit(resp2.reference);
				},
				onCancel: () => {
					module.open(Dialogue, {
						status: 400,
						title: 'Payment Canceled',
						messages: `The payment process was canceled`,
						button: [
							{
								name: 'Ok',
								icon: 'ok',
								fn: () => {
									module.close();
								}
							}
						]
					});
				}
			});
			paystack.openIframe();
		} else {
			error = resp;
		}
	};

	const submit = async (reference) => {
		error = {};

		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({
				reference,
				email_template_admin: email_template_admin.innerHTML.replace(/&amp;/g, '&'),
				email_template_user: email_template_user.innerHTML.replace(/&amp;/g, '&')
			})
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.cart_items = [];
			goto(`/orders/${resp.order.key}`);

			module.open(Dialogue, {
				status: 200,
				title: 'Successful',
				message: `Your order was placed successfully`,
				buttons: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							module.close();
						}
					}
				]
			});
		} else {
			error = resp;
		}
	};
</script>

<svelte:head>
	<script src="https://js.paystack.co/v2/inline.js"></script>
</svelte:head>

<Next
	value={total + Number(ops.cart.cost_delivery)}
	label="Total Amount"
	btn_label="Make Payment"
	icon="cart"
	onclick={make_payment}
>
	<Note note={error.error} status="400" --note-margin-top="16px"></Note>

	<span class="terms">
		by clicking the order button, you have accepred our
		<Link href="/terms" --link-font-size="0.8rem">terms and conditions</Link>
	</span>
</Next>

<div bind:this={email_template_admin} style="display: none;">
	<Email_Admin order={ops.cart} items={app.cart_items} />
</div>
<div bind:this={email_template_user} style="display: none;">
	<Email_User order={ops.cart} items={app.cart_items} />
</div>

<style>
	.terms {
		font-size: small;
	}
</style>
