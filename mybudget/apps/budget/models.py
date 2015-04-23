# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import models, transaction


class Accounts(models.Model):
    name = models.CharField(max_length=255)
    current_amount = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = _(u'Счет')
        verbose_name_plural = _(u'Счета')

    def __unicode__(self):
        return u'%(name)s %(amount)s' % {'name': self.name, 'amount': self.current_amount}


class RegularMonthlyExpenses(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    account = models.ForeignKey(Accounts, null=True)

    class Meta:
        verbose_name = u'Постоянный месячный расход'
        verbose_name_plural = u'Постоянные месячные расходы'

    def __unicode__(self):
        return u'%s %s' % (self.name, self.amount)


class Envelopes(models.Model):
    name = models.CharField(max_length=255)
    current_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    monthly_replenishment = models.DecimalField(max_digits=8, decimal_places=2)
    cash = models.BooleanField()
    account = models.ForeignKey(Accounts, null=True)
    closed = models.BooleanField()
    onetime_envelope = models.BooleanField()
    max_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = u"конверт"
        verbose_name_plural = u'Конверты'
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return '/%i/' % self.id


class Expenses(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    envelope = models.ForeignKey(Envelopes)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'Расход'
        verbose_name_plural = u'Расходы'

    def __unicode__(self):
        return u'%s ' % self.name

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                envelope = Envelopes.objects.get(name=self.envelope)
                envelope.current_amount = envelope.current_amount - self.amount
                envelope.save()
                if envelope.cash is False:
                    account = Accounts.objects.get(id=envelope.account.id)
                    account.current_amount = account.current_amount - self.amount
                    account.save()
                super(Expenses, self).save(*args, **kwargs)
                print 'transaction goes!'
        except:
            'Something goes wrong!'

    def get_absolute_url(self):
        return '/%i/' % self.id


class Incomes(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    account = models.ForeignKey(Accounts, null=True)

    class Meta:
        verbose_name = u'Доход'
        verbose_name_plural = u'Доходы'

    def __unicode__(self):
        return u'%s' % self.amount


