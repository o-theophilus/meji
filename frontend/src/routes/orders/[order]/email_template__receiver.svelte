<script>
	export let order;
</script>

<b>Receiver</b>
<br />
Name:
{order.receiver.name}
<br />
Phone:
{order.receiver.phone}
<br />
Address:
{order.receiver.address.line},
{order.receiver.address.local_area},
{order.receiver.address.state},
{order.receiver.address.country},
{order.receiver.address.postal_code}.
