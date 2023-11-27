<script>
	import { page } from '$app/stores';

	import { user } from '$lib/store.js';
	import Template from '$lib/email_template.svelte';
	import Items from '../orders/[order]/email_template__items.svelte';
	import Receiver from '../orders/[order]/email_template__receiver.svelte';
	import Eta from '../orders/[order]/email_template__eta.svelte';

	export let order;
</script>

<Template>
	Dear Admin
	<br />
	<br />
	Kindly see order:
	<a
		style="
	text-decoration: none;
	color: #1d9bf0;
	"
		href="{$page.url.origin}/orders/{'{'}order_key{'}'}"
		target="_blank"
	>
		{'{'}order_key{'}'}
	</a>
	information below:
	<br />
	<br />
	<b>User</b>
	<br />
	Name:
	<a
		style="
text-decoration: none;
color: #1d9bf0;
"
		href="{$page.url.origin}/profile?search={$user.key}"
		target="_blank"
	>
		{$user.name}
	</a>
	<br />
	Phone:
	{$user.phone}
	<br />
	Email:
	{$user.email}
	<br />
	<br />
	<Receiver {order} />
	<br />
	<Eta {order} />
	<br />
	<br />
	<Items {order} />
	<br />
	<br />
	Best regards,
	<br />
	<br />
	<b> Meji </b>
</Template>
